from database.connection import get_session
from fastapi import Depends
from database.models import Companies,ResearchRun, Compititors, PricingData, BattleCard
from schema import AgentState
from sqlmodel import Session

from fastapi import Depends
from sqlmodel import Session, select
from decimal import Decimal, InvalidOperation
import re


def parse_starter_price(raw_price) -> Decimal:
    """Extract a clean Decimal from free-text pricing strings like
    '$25/month', '$ 24.90 / user / month', 'Contact Sales', or None.
    Falls back to Decimal('0.00') when no number can be found, since
    the starter_price column is NOT NULL.
    """
    if not raw_price or not isinstance(raw_price, str):
        return Decimal("0.00")

    # Grab the first number in the string (handles "24.90", "1,000", etc.)
    match = re.search(r"[\d,]+\.?\d*", raw_price)
    if not match:
        return Decimal("0.00")

    number_str = match.group(0).replace(",", "")

    try:
        return Decimal(number_str)
    except InvalidOperation:
        return Decimal("0.00")


def save_company_and_run(
    state: AgentState, session: Session = Depends(get_session)
) -> dict:

    # 1. Check if the company already exists via its unique website URL
    home_url = state["urls"].home_url
    statement = select(Companies).where(Companies.website == home_url)
    existing_company = session.exec(statement).first()

    # check for exist company
    if existing_company:
        db_company = existing_company
    else:
        db_company = Companies(
            name=state["company_name"],
            website=home_url,
            description=state["description"],
        )
        session.add(db_company)
        session.flush()

    # 2. Create the ResearchRun
    db_run = ResearchRun(
        company_id=db_company.id,
        status="completed",
    )

    session.add(db_run)
    session.flush()
    
    # 3. Create the Competitors (only for new companies, only if we have names)
    if not existing_company and state["competitors"]:
        for comp_name in state["competitors"]:
            db_compit = Compititors(
                company_id=db_company.id,
                compititors_name=comp_name
            )

            session.add(db_compit)
    
    # 4. Create the Pricing Model (every run, not just repeat companies)
    if state.get("pricing_info"):
        db_price = PricingData(
            company_id=db_company.id,
            free_tier=state["pricing_info"].free_tier,
            starter_price=parse_starter_price(state["pricing_info"].starter_plan.price),
            enterprise_plan= state["pricing_info"].enterprise_plan
        )
        session.add(db_price)
    
    # 5. Create the Battle Card (every run, not just repeat companies)
    db_card = BattleCard(
        company_id= db_company.id,
        battle_card= state["final_report"]
    )
    session.add(db_card)
    
    session.commit()
    session.refresh(db_company)
    
    return {
        "message":"Company Data Saved Successfully"
    }