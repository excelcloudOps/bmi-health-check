"""BMI calculation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BmiResult:
    bmi: float
    category: str
    height_cm: float
    weight_kg: float


def categorize_bmi(bmi: float) -> str:
    """Return WHO-style adult BMI category."""
    if bmi < 18.5:
        return "underweight"
    if bmi < 25.0:
        return "normal"
    if bmi < 30.0:
        return "overweight"
    return "obese"


def calculate_bmi(height_cm: float, weight_kg: float) -> BmiResult:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("height_cm and weight_kg must be positive numbers")

    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)
    bmi_rounded = round(bmi, 1)
    return BmiResult(
        bmi=bmi_rounded,
        category=categorize_bmi(bmi_rounded),
        height_cm=height_cm,
        weight_kg=weight_kg,
    )
