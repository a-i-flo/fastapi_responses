from typing import Dict
from models import Rat, DailyResponse


DS: Dict[str, Rat] = {
    "rat1": Rat(
        ratnumber = 1,
        group = "High",
        responses = [DailyResponse(day=1, lever=22, nosepokes=50),
                       DailyResponse(day=2, lever=2, nosepokes=55),
                       DailyResponse(day=3, lever=5, nosepokes=40),
                       DailyResponse(day=4, lever=33, nosepokes=22)],
    ),
    "rat2": Rat(
        ratnumber = 2,
        group = "High",
        responses = [DailyResponse(day=1, lever=42, nosepokes=6),
                       DailyResponse(day=2, lever=35, nosepokes=33),
                       DailyResponse(day=3, lever=73, nosepokes=9),
                       DailyResponse(day=4, lever=12, nosepokes=11)],
    ),
    "rat3": Rat(
        ratnumber = 3,
        group = "Low",
        responses = [DailyResponse(day=1, lever=5, nosepokes=62),
                       DailyResponse(day=2, lever=43, nosepokes=63),
                       DailyResponse(day=3, lever=11, nosepokes=23),
                       DailyResponse(day=4, lever=10, nosepokes=2)],
    )

}