def calculate_retirement_corpus(
    current_age: int,
    retirement_age: int,
    current_savings: float,
    monthly_investment: float,
    expected_annual_return: float,
) -> dict[str, float]:
    """Estimate retirement corpus and a sustainable annual income (4% rule).

    Assumptions:
    - Monthly investments are made at the end of each month.
    - Expected annual return is applied as monthly compounding.
    - Estimated retirement income uses a 4% rule (educational estimate).
    """

    years = retirement_age - current_age
    if years <= 0:
        raise ValueError("Retirement age must be greater than current age")
    if current_savings < 0:
        raise ValueError("Current savings cannot be negative")
    if monthly_investment < 0:
        raise ValueError("Monthly investment cannot be negative")
    if expected_annual_return < 0:
        raise ValueError("Expected annual return cannot be negative")

    months = years * 12
    monthly_rate = expected_annual_return / 100.0 / 12.0

    # Future value of current savings
    if monthly_rate == 0:
        fv_current = current_savings
    else:
        fv_current = current_savings * ((1.0 + monthly_rate) ** months)

    # Future value of monthly investments (ordinary annuity)
    if monthly_rate == 0:
        fv_monthly = monthly_investment * months
    else:
        fv_monthly = monthly_investment * (((1.0 + monthly_rate) ** months - 1.0) / monthly_rate)

    retirement_corpus = round(fv_current + fv_monthly, 2)

    # Estimated sustainable annual income using 4% rule
    estimated_annual_income = round(retirement_corpus * 0.04, 2)

    return {
        "retirement_corpus": retirement_corpus,
        "estimated_annual_income": estimated_annual_income,
    }
