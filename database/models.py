from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func, Numeric
from typing import Optional
from decimal import Decimal

class Companies(SQLModel, table=True):
    __tablename__ = "companies"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name:str
    website: str = Field(unique=True)
    description:str
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True,
            )
    )
    
    research_runs: list["ResearchRun"] = Relationship(back_populates="company")
    
    battle_cards: list["BattleCard"] = Relationship(back_populates= "company")

class ResearchRun(SQLModel, table=True):
    __tablename__: str = "research_runs"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    company_id: uuid.UUID = Field(
        foreign_key="companies.id"
    )
    
    company: Companies = Relationship(
        back_populates="research_runs"
    )
    
    status: str = Field(default="pending", index=True)

    # Automatically set by the database on row creation
    started_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True,
        )
    )

    completed_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=True,
        )
    )

class Compititors(SQLModel, table=True):
    __tablename__ = "compititors"

    id: uuid.UUID =  Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    company_id: uuid.UUID = Field(
        foreign_key="companies.id"
    )
    compititors_name: str =Field(
        nullable=True
    )

class PricingData(SQLModel,table=True):
    __tablename__ = "pricing_data"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    company_id: uuid.UUID = Field(
        foreign_key="companies.id"
    )
    free_tier: bool = Field(default=False)
    starter_price: Optional[Decimal] = Field(
        default=Decimal("0.00"),
        sa_column=Column(Numeric(precision=10, scale=2), nullable=False),
    )
    enterprise_plan: bool = Field(default=False)

class BattleCard(SQLModel, table=True):
    __tablename__ = "battle_card"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    company_id: uuid.UUID = Field(
        foreign_key="companies.id"
    )
    battle_card: str
    created_at: datetime = Field(
        sa_column= Column(
            DateTime(timezone=True),
            index=True,
            server_default=func.now(),
            nullable=False
        )
    )
    
    company: Companies = Relationship(
        back_populates="battle_cards"
    )
    