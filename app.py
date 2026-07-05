from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from config import logger
from bt_card import run_battle_card_generator

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Battle Card API is starting up...")
    yield
    logger.info("Battle Card API is shutting down...")


app = FastAPI(
    title="Battle Card Generator API",
    description="Provide a company name and receive a structured competitive Battle Card.",
    version="1.0.0",
    lifespan=lifespan,
)


class BattleCardRequest(BaseModel):
    company_name: str = Field(
        ...,
        min_length=1,
        description="The name of the company to research.",
        examples=["OpenAI"],
    )


class BattleCardResponse(BaseModel):
    status: str = Field(description="'success' or 'error'")
    company: str = Field(description="The company name that was researched.")
    data: str = Field(description="The full Battle Card report in Markdown format.")


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "running", "message": "Battle Card Generator API is live."}


@app.post(
    "/generate-card",
    response_model=BattleCardResponse,
    tags=["Battle Card"],
    summary="Generate a Battle Card for a company",
    description=(
        "Accepts a company name, runs the full research pipeline "
        "(web search, pricing scrape, news scrape), and returns "
        "a competitive Battle Card in Markdown."
    ),
)
async def generate_battle_card(request: BattleCardRequest):
    company = request.company_name.strip()

    logger.info(f"Received request to generate Battle Card for: '{company}'")

    result = await run_battle_card_generator(company)

    if result is None:
        logger.error(f"Battle Card generation returned None for: '{company}'")
        raise HTTPException(
            status_code=500,
            detail=f"Battle Card generation failed for '{company}'. Check server logs.",
        )

    final_report = result.get("final_report", "")

    if not final_report or final_report.startswith("# Error Generating Battle Card"):
        logger.error(f"Battle Card writer node failed for: '{company}'")
        raise HTTPException(
            status_code=502,
            detail=f"The report writer failed for '{company}'. Check server logs.",
        )

    logger.info(f"Successfully generated Battle Card for: '{company}'")

    return BattleCardResponse(
        status="success",
        company=company,
        data=final_report,
    )