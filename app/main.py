"""FastAPI BMI health-check service."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.bmi import calculate_bmi

app = FastAPI(title="BMI Health Check", version="1.0.0")


class BmiRequest(BaseModel):
    height_cm: float = Field(..., gt=0, description="Height in centimeters")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")


class BmiResponse(BaseModel):
    height_cm: float
    weight_kg: float
    bmi: float
    category: str


class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/bmi", response_model=BmiResponse)
def bmi_post(body: BmiRequest) -> BmiResponse:
    try:
        result = calculate_bmi(body.height_cm, body.weight_kg)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BmiResponse(
        height_cm=result.height_cm,
        weight_kg=result.weight_kg,
        bmi=result.bmi,
        category=result.category,
    )


@app.get("/bmi", response_model=BmiResponse)
def bmi_get(
    height_cm: float = Query(..., gt=0),
    weight_kg: float = Query(..., gt=0),
) -> BmiResponse:
    try:
        result = calculate_bmi(height_cm, weight_kg)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BmiResponse(
        height_cm=result.height_cm,
        weight_kg=result.weight_kg,
        bmi=result.bmi,
        category=result.category,
    )
