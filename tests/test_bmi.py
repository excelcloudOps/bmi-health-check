from app.bmi import calculate_bmi, categorize_bmi
import pytest


def test_normal_bmi():
    result = calculate_bmi(175, 70)
    assert result.bmi == 22.9
    assert result.category == "normal"


def test_underweight():
    result = calculate_bmi(180, 50)
    assert result.category == "underweight"


def test_overweight():
    result = calculate_bmi(170, 80)
    assert result.category == "overweight"


def test_obese():
    result = calculate_bmi(160, 90)
    assert result.category == "obese"


def test_rejects_non_positive():
    with pytest.raises(ValueError):
        calculate_bmi(0, 70)
    with pytest.raises(ValueError):
        calculate_bmi(170, -1)


def test_categorize_boundaries():
    assert categorize_bmi(18.4) == "underweight"
    assert categorize_bmi(18.5) == "normal"
    assert categorize_bmi(24.9) == "normal"
    assert categorize_bmi(25.0) == "overweight"
    assert categorize_bmi(29.9) == "overweight"
    assert categorize_bmi(30.0) == "obese"
