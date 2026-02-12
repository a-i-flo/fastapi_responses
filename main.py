
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Mapping, Optional

from stats import daily_averages
from schemas import DailyAverages
from models import Rat
from data import DS
from models import GroupType

app = FastAPI(title="Rat Metrics API", version="1.0.0")

def get_rat_or_404(data: Mapping[str, Rat], rat_id: str) -> Rat:
    rat = data.get(rat_id)
    if not rat:
        raise HTTPException(status_code=404, detail="Rat not found")
    return rat


# Endpoints
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/rats/{rat_id}", response_model=Rat)
def get_rat(rat_id: str):
    return get_rat_or_404(DS, rat_id)

@app.get("/daily/average", response_model=DailyAverages)
def get_daily_average(group: Optional[GroupType] = Query(None)):
    return daily_averages(DS, group=group)









