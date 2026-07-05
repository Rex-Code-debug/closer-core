from pydantic import BaseModel, Field
from typing import List,Optional

class Urls(BaseModel):
    home_url: str = Field(description="Official home url of website")
    pricing_url: str = Field(description="Url of pricing page")
    info_url: Optional[str] = Field(description= "Url of information gathering page like blog, news, newsletter ...")

class CompanyResearch(BaseModel):
    website_url: str = Field(description="Official website URL of the company")
    description: str = Field(description="One sentence description of what the company does")
    competitors: List[str] = Field(description="List of competitor company names")
    pricing_url: str = Field(description="Url of pricing page")
    info_url: Optional[str] = Field(description= "Url of blog page")
    

class StarterPlan(BaseModel):
    name: Optional[str] = Field(description="The cheapest paid plan name e.g. Pro, Basic, Starter")
    price: Optional[str] = Field(description="Price with currency e.g. $7.25/month, ₹500/month")

class PricingInfo(BaseModel):
    free_tier: bool = Field(description="True if a free plan exists ($0 or free forever)")
    starter_plan: StarterPlan = Field(description="The cheapest paid plan after the free tier")
    enterprise_plan: bool = Field(description="True if enterprise or custom pricing exists")

class Headline(BaseModel):
    title: str = Field(description="The headline or article title text")
    position: int = Field(description="Position/rank of the headline, starting from 1")


class NewsHeadlines(BaseModel):
    headlines: List[Headline] = Field(description="Top 3 most prominent headlines or article titles")