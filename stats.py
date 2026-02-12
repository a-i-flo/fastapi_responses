from typing import Dict, Optional
from schemas import DailyAverages, DailyAveragesRow
from models import GroupType
from models import Rat  # wherever Rat is defined

def daily_averages(data: Dict[str, Rat], group: Optional[GroupType] = None) -> DailyAverages:
    # optional filter
    rats = list(data.values())
    if group is not None:
        rats = [r for r in rats if r.group == group]

    # group values by day for BOTH metrics
    lever_grouped = {}
    nose_grouped = {}

    for rat in rats:
        for d in rat.responses:  # or rat.responses if you rename it
            # lever
            if d.day not in lever_grouped:
                lever_grouped[d.day] = []
            lever_grouped[d.day].append(d.lever)

            # nosepokes
            if d.day not in nose_grouped:
                nose_grouped[d.day] = []
            nose_grouped[d.day].append(d.nosepokes)

    # build rows (sorted by day)
    days = sorted(set(lever_grouped.keys()) | set(nose_grouped.keys()))
    rows = []
    for day in days:
        lever_vals = lever_grouped.get(day, [])
        nose_vals = nose_grouped.get(day, [])

        # if a day is missing data, you can skip or handle differently
        if not lever_vals or not nose_vals:
            continue

        rows.append(
            DailyAveragesRow(
                day=day,
                lever_mean=sum(lever_vals) / len(lever_vals),
                nosepokes_mean=sum(nose_vals) / len(nose_vals),
            )
        )

    return DailyAverages(group=group, rows=rows)
