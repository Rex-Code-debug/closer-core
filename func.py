from config import logger
from asyncddgs import aDDGS
from tavily import AsyncTavilyClient
from config import settings
import asyncio

SCRAPE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

# search_tool
async def search_tool(query:str,max_result:int = 3) -> dict:
    async with aDDGS(headers=SCRAPE_HEADERS) as addgs:
        try:
            results = await addgs.text(query, max_results=max_result)
            if not results:
                return "not found"
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"

        return results

# Scraping func


tav = AsyncTavilyClient(api_key=settings.tavily_key)

async def scrape_website(url: str) -> str:
    response = await tav.extract(urls=url)

    if response["results"]:
        return response["results"][0]["raw_content"]

    return ""