def calculate_emergency_fund(monthly_expenses: float, emergency_coverage_months: int) -> dict[str, float]:
    """Compute recommended emergency fund.

    Recommended fund = monthly_expenses * emergency_coverage_months
    """
    if monthly_expenses <= 0:
        raise ValueError("Monthly expenses must be greater than 0")
    if emergency_coverage_months <= 0:
        raise ValueError("Emergency coverage months must be greater than 0")

    recommended = monthly_expenses * emergency_coverage_months

    return {"recommended_emergency_fund": round(recommended, 2)}

