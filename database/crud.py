from database.connection import get_session
from fastapi import Depends
from database.models import Companies,ResearchRun, Compititors, PricingData, BattleCard
from schema import AgentState
from sqlmodel import Session

from fastapi import Depends
from sqlmodel import Session, select


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
    
    # 3. Create the Competitors
    if state["competitors"] and not existing_company:
        for comp_name in state["competitors"]:
            db_compit = Compititors(
                company_id=db_company.id,
                compititors_name=comp_name
            )

            session.add(db_compit)
    else:
        db_compit = Compititors(
            company_id=db_company.id,
            compititors_name= None
        )
        session.add(db_compit)
    
    # 4. Create the Pricing Model
    if existing_company:
        if state.get("pricing_info"):
            db_price = PricingData(
                company_id=db_company.id,
                free_tier=state["pricing_info"].free_tier,
                starter_price= state["pricing_info"].starter_plan.price,
                enterprise_plan= state["pricing_info"].enterprise_plan
            )
            session.add(db_price)
    
    # 5. Create the Battle Card
    if existing_company:
        db_card = BattleCard(
            company_id= db_company.id,
            battle_card= state["final_report"]
        )
    
    session.commit()
    session.refresh()
    
    return {
        "message":"Company Data Saved Successfully"
    }
            