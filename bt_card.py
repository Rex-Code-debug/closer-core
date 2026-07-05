import operator
import aiofiles
from schema import CompanyResearch,PricingInfo,NewsHeadlines, Urls
from langchain_groq import ChatGroq
from typing import List, Annotated, TypedDict, Dict, Any
from langchain_core.messages import BaseMessage
from func import search_tool, scrape_website
from langgraph.graph import StateGraph, START, END
from config import settings, logger 

api_key = settings.groq_api_key

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    api_key=api_key
)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    company_name: str
    urls: Urls
    description: str
    competitors: list[str]
    pricing_info: List[Dict[str, Any]]
    news_headlines: list
    loop_count: int
    final_report: str


async def research_node(state: AgentState):
    """Search for company's official website, description, and competitors."""
    query = state["company_name"]
    count = state.get("loop_count", 0)

    logger.info(f"Searching about {query}")

    structured_model = model.with_structured_output(CompanyResearch)

    try:
        comp_results = await search_tool(f"{query} official website competitors")
        price_results = await search_tool(f"pricing page of {query}")
        info_res = await search_tool(f"{query} blog page",1)
        
        prompt = f"""From these search results, extract the official website URL, pricing page url, information url, a 1-sentence description of what they do, and list of competitors for {query}.

Search results:
{comp_results} + {price_results} + {info_res}"""

        result: CompanyResearch = await structured_model.ainvoke(prompt)

        logger.info(f"Found website: {result.website_url}")

    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        result = CompanyResearch(
            website_url="Not found",
            description="Not available",
            competitors=[],
            pricing_url="Not found",
            info_url="Not found",
        )

    return {
        "urls": Urls(
    home_url=result.website_url,
    pricing_url=result.pricing_url,
    info_url=result.info_url,
),
        "description": result.description,
        "competitors": result.competitors,
        "loop_count": count + 1,
    }

async def pricing_node(state: AgentState):
    """Extract pricing information from pricing page"""
    pricing_info = state.get("pricing_info", [])
    url = state.get("urls", "")
    pricing_url = url.pricing_url

    if not url or pricing_url == "Not found":
        logger.error("No valid home URL and pricing url found skipping pricing extraction")
        return {"pricing_info": pricing_info}

    text = None

    try:
        logger.info(f"Trying pricing URL: {pricing_url}")
        text = await scrape_website(pricing_url)
        if text and len(text) > 100:
            logger.info(f"Successfully fetched content from: {pricing_url}")

    except Exception as e:
        logger.exception(f"Failed to fetch {url}: {str(e)}")

    if not text:
        logger.error("No content retrieved from pricing page")
        return {"pricing_info": pricing_info}

    try:
        clean_text = text[1000:8000]

        prompt = f"""You are a pricing research expert. Analyze the following pricing page content and extract specific details.

PRICING PAGE CONTENT:
{clean_text}

RULES:
- For "free_tier": return true if there's a free plan (look for "free", "free forever", "$0"), otherwise false
- For "starter_plan": Find the CHEAPEST paid plan after free tier and include:
  * "name": the plan name (e.g., "Pro", "Basic", "Plus", "Starter")
  * "price": the price with currency (e.g., "$7.25/month", "₹500/month")
  * If not found, use null for both fields
- For "enterprise_plan": return true if enterprise/custom pricing exists (look for "Enterprise", "Custom", "Contact Sales"), otherwise false"""

        structured_model = model.with_structured_output(PricingInfo)
        result: PricingInfo = await structured_model.ainvoke(prompt)

        pricing_info.append(result)
        logger.info("Successfully extracted pricing information")

    except Exception as e:
        logger.exception(f"Error in pricing_node: {str(e)}")

    return {"pricing_info": pricing_info}


async def news_node(state: AgentState):
    """Extract top 3 news headlines from blog page"""

    urls = state.get('urls', '')
    news_url = urls.info_url

    if not urls or news_url == "Not found":
        logger.error("No valid home URL found, skipping news extraction")
        return {"news_headlines": []}

    text = None
    try:
        logger.info(f"Trying news URL: {news_url}")
        text = await scrape_website(news_url)
        if text and len(text) > 100:
            logger.info(f"Successfully fetched content from: {news_url}")

    except Exception as e:
            logger.exception(f"Failed to fetch {news_url}: {str(e)}")

    if not text:
        logger.error("No content retrieved from any news/blog page")
        return {"news_headlines": []}

    try:
        clean_text = text[:5000]

        prompt = f"""You are a content analyst expert. Analyze the following blog/news page content and extract the top 3 headlines with 1 line briefing about each lines.

CONTENT:
{clean_text}

RULES:
- Find actual headlines or titles of articles or blog posts
- Headlines should be clear and complete phrases
- Prioritize the most recent or featured articles
- Do not include navigation text, menu items, or generic labels
- Each headline should represent an actual article
- If fewer than 3 headlines are found, return only what you find
- Write brief 1 line about each healines explaing what is for that headline"""

        structured_model = model.with_structured_output(NewsHeadlines)
        result: NewsHeadlines = await structured_model.ainvoke(prompt)

        logger.info(f"Successfully extracted {len(result.headlines)} headlines")
        return {"news_headlines": result.headlines}

    except Exception as e:
        logger.exception(f"Error in news_node: {str(e)}")
        return {"news_headlines": []}


async def writer_node(state: AgentState):
    """Generate and save the final Battle Card report."""

    model_writer = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=api_key
    )

    company_name = state.get("company_name", "Unknown Company")
    description = state.get("description", "Not available")
    competitors = state.get("competitors", [])
    pricing_info = state.get("pricing_info", [])
    news_headlines = state.get("news_headlines", [])
    urls = state.get("urls", "Not found")

    # Formating competitors
    competitors_text = ", ".join(competitors) if competitors else "Unknown"

    # Formating pricing
    if pricing_info:
        pricing_data: PricingInfo = pricing_info[0]
        free_tier = "Yes" if pricing_data.free_tier else "No"
        starter_plan = pricing_data.starter_plan
        starter_text = (
            f"{starter_plan.name}: {starter_plan.price}"
            if starter_plan and starter_plan.name and starter_plan.price
            else "Unknown"
        )
        enterprise = "Available" if pricing_data.enterprise_plan else "Not Available"
        pricing_text = f"""
- **Free Tier:** {free_tier}
- **Starter Plan:** {starter_text}
- **Enterprise Plan:** {enterprise}
"""
    else:
        pricing_text = "Unknown"

    # Formating headlines
    if news_headlines:
        news_text = "\n".join([
            f"{i + 1}. {headline.title}"
            for i, headline in enumerate(news_headlines)
        ])
    else:
        news_text = "No recent news available"

    prompt = f"""You are a Sales Assistant. Write a professional Battle Card for {company_name}.

INSTRUCTIONS:
- Use ONLY the data provided below
- Do NOT hallucinate or add information not present in the data
- Keep it concise and sales-focused
- Use markdown formatting for readability
- If any information is missing or "Unknown", clearly state it as such

DATA PROVIDED:
---
Company: {company_name}
Website: {urls}
Description: {description}
Competitors: {competitors_text}

Pricing Information:
{pricing_text}

Recent News/Blog Headlines:
{news_text}
---

BATTLE CARD LAYOUT:

# Battle Card: {company_name}

## 1. What They Do
[Brief description of the company and their main offering]

## 2. Key Competitors
[List the main competitors]

## 3. Pricing Structure
[Detail the pricing information available]

## 4. Recent News & Updates
[List recent headlines or news]

## 5. Sales Strategy Tips
[Brief insights on how to position against competitors based on the data]

---
Write the complete battle card now:"""

    logger.info(f"Generating Battle Card for {company_name}...")

    try:
        response = await model_writer.ainvoke(prompt)
        battle_card = response.content

        # Async file writing
        filename = f"cards/{company_name.replace(' ', '_').lower()}_battle_card.md"
        async with aiofiles.open(filename, "w", encoding="utf-8") as f:
            await f.write(battle_card)

        logger.info(f"Battle Card saved to {filename}")

        return {
            "final_report": battle_card,
            "loop_count": state.get("loop_count", 0) + 1
        }

    except Exception as e:
        logger.exception(f"Error generating battle card: {str(e)}")
        return {
            "final_report": f"# Error Generating Battle Card\n\nError: {str(e)}",
            "loop_count": state.get("loop_count", 0) + 1
        }

# Build the graph
builder = StateGraph(AgentState)

# Adding nodes
builder.add_node("detective", research_node)
builder.add_node("pricing", pricing_node)
builder.add_node("news", news_node)
builder.add_node("editor", writer_node)

# Adding edges to define the workflow
builder.add_edge(START,"detective")
builder.add_edge("detective", "pricing")
builder.add_edge("pricing", "news")
builder.add_edge("news", "editor")
builder.add_edge("editor", END)

# Compiling the graph
graph = builder.compile()

async def run_battle_card_generator(company_name: str):
    """Runs the battle card generator for a given company."""
    initial_state = {
        "messages": [],
        "company_name": company_name,
        "urls": Urls(
            home_url="",
            pricing_url="",
            info_url=""
        ),
        "description": "",
        "competitors": [],
        "pricing_info": [],
        "news_headlines": [],
        "loop_count": 0,
        "final_report": ""
    }
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Starting Battle Card Generation for: {company_name}")
    logger.info(f"{'='*60}\n")
    
    try:
        result = await graph.ainvoke(initial_state)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Battle Card Generation Complete!")
        logger.info(f"{'='*60}\n")
        
        return result
    except Exception as e:
        logger.exception(f"\nError during execution: {str(e)}")
        return None

# Test run
# async def main():
#     company_name = input("Enter company name: ")
#     result = await run_battle_card_generator(company_name)

#     if result:
#         logger.info("\n📊 Final Report Preview:")
#         logger.info("-" * 60)
#         logger.info(result.get("final_report", "No report generated")[:500] + "...")

# if __name__ == "__main__":
#     asyncio.run(main())