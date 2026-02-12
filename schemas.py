from typing import Optional, List, Optional
from pydantic import BaseModel
from models import GroupType



class DailyAveragesRow(BaseModel):
    day: int
    lever_mean: float
    nosepokes_mean: float

class DailyAverages(BaseModel):
    group: Optional[GroupType] = None
    rows: List[DailyAveragesRow]

