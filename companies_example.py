from __future__ import annotations

from typing import Dict, List, Literal, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Company Metrics API", version="1.0.0")

CompanySize = Literal["small", "mid", "large"]


# ---------- Data models (schemas) ----------
class YearMetric(BaseModel):
    year: int
    revenue: float = Field(..., ge=0, description="Revenue for the year (e.g., in GBP)")
    pct_change: Optional[float] = Field(
        None,
        description="Percent change from previous year. None if no prior year.",
    )


class Company(BaseModel):
    id: str
    name: str
    size: CompanySize
    metrics: List[YearMetric]


class CompanySummary(BaseModel):
    id: str
    name: str
    size: CompanySize


# ---------- Mock dataset ----------
DB: Dict[str, Company] = {
    "comp_001": Company(
        id="comp_001",
        name="Northbridge Analytics",
        size="mid",
        metrics=[
            YearMetric(year=2021, revenue=5_200_000, pct_change=None),
            YearMetric(year=2022, revenue=5_850_000, pct_change=12.5),
            YearMetric(year=2023, revenue=6_200_000, pct_change=6.0),
            YearMetric(year=2024, revenue=5_900_000, pct_change=-4.8),
        ],
    ),
    "comp_002": Company(
        id="comp_002",
        name="Pine & Co Retail",
        size="small",
        metrics=[
            YearMetric(year=2021, revenue=650_000, pct_change=None),
            YearMetric(year=2022, revenue=720_000, pct_change=10.8),
            YearMetric(year=2023, revenue=690_000, pct_change=-4.2),
            YearMetric(year=2024, revenue=810_000, pct_change=17.4),
        ],
    ),
    "comp_003": Company(
        id="comp_003",
        name="Horizon Manufacturing Group",
        size="large",
        metrics=[
            YearMetric(year=2021, revenue=120_000_000, pct_change=None),
            YearMetric(year=2022, revenue=126_000_000, pct_change=5.0),
            YearMetric(year=2023, revenue=131_500_000, pct_change=4.4),
            YearMetric(year=2024, revenue=129_000_000, pct_change=-1.9),
        ],
    ),
    "comp_004": Company(
        id="comp_004",
        name="Beacon Health Devices",
        size="mid",
        metrics=[
            YearMetric(year=2021, revenue=9_800_000, pct_change=None),
            YearMetric(year=2022, revenue=10_300_000, pct_change=5.1),
            YearMetric(year=2023, revenue=11_900_000, pct_change=15.5),
            YearMetric(year=2024, revenue=13_400_000, pct_change=12.6),
        ],
    ),
    "comp_005": Company(
        id="comp_005",
        name="CloudSprout SaaS",
        size="small",
        metrics=[
            YearMetric(year=2021, revenue=1_100_000, pct_change=None),
            YearMetric(year=2022, revenue=1_650_000, pct_change=50.0),
            YearMetric(year=2023, revenue=2_050_000, pct_change=24.2),
            YearMetric(year=2024, revenue=2_000_000, pct_change=-2.4),
        ],
    ),
}


# ---------- Helpers ----------
def get_company_or_404(company_id: str) -> Company:
    company = DB.get(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


# ---------- Endpoints ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/companies", response_model=List[CompanySummary])
def list_companies(
    size: Optional[CompanySize] = Query(None, description="Filter by company size"),
    q: Optional[str] = Query(None, description="Search by substring in company name"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    List companies (summary view), with optional filtering and pagination.
    """
    companies = list(DB.values())

    if size:
        companies = [c for c in companies if c.size == size]

    if q:
        q_lower = q.lower()
        companies = [c for c in companies if q_lower in c.name.lower()]

    paged = companies[offset : offset + limit]
    return [CompanySummary(id=c.id, name=c.name, size=c.size) for c in paged]


@app.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: str):
    """
    Get a single company, including its full metric history.
    """
    return get_company_or_404(company_id)


@app.get("/companies/{company_id}/revenue")
def revenue_history(
    company_id: str,
    start_year: Optional[int] = Query(None),
    end_year: Optional[int] = Query(None),
):
    """
    Return revenue + pct_change, optionally filtered by year range.
    """
    company = get_company_or_404(company_id)
    metrics = company.metrics

    if start_year is not None:
        metrics = [m for m in metrics if m.year >= start_year]
    if end_year is not None:
        metrics = [m for m in metrics if m.year <= end_year]

    return {
        "company_id": company.id,
        "name": company.name,
        "size": company.size,
        "metrics": metrics,
    }


@app.get("/companies/{company_id}/latest")
def latest_metrics(company_id: str):
    """
    Return the most recent year metric for a company.
    """
    company = get_company_or_404(company_id)
    latest = max(company.metrics, key=lambda m: m.year)
    return {"company_id": company.id, "year": latest.year, "revenue": latest.revenue, "pct_change": latest.pct_change}


@app.get("/stats/revenue")
def revenue_stats(year: int = Query(..., description="Year to compute stats for")):
    """
    Cross-company stats for a given year.
    """
    rows = []
    for c in DB.values():
        m = next((m for m in c.metrics if m.year == year), None)
        if m:
            rows.append({"company_id": c.id, "name": c.name, "size": c.size, "revenue": m.revenue})

    if not rows:
        raise HTTPException(status_code=404, detail=f"No data found for year={year}")

    revenues = [r["revenue"] for r in rows]
    return {
        "year": year,
        "count": len(rows),
        "min": min(revenues),
        "max": max(revenues),
        "average": sum(revenues) / len(revenues),
        "rows": rows,
    }

