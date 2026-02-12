
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


GroupType = Literal["High", "Low"]

class DailyResponse(BaseModel):
    day: int
    lever: int = Field(..., ge=0)
    nosepokes: int = Field(..., ge=0)


class Rat(BaseModel):
    ratnumber: int
    group: GroupType
    responses: List[DailyResponse]