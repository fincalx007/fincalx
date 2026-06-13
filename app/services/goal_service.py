def calculate_goal_monthly(goal_amount: float, years: int, expected_annual_return: float) -> dict[str, float]:
    """Calculate required monthly investment to reach a goal amount.

    Uses future value of an ordinary annuity formula:
    PMT = FV * r / ((1+r)**n - 1)
    where r = monthly_rate, n = months
    """
    if years <= 0:
        raise ValueError("Time horizon must be greater than 0")
    if goal_amount <= 0:
        raise ValueError("Goal amount must be greater than 0")
    if expected_annual_return < 0:
        raise ValueError("Expected annual return cannot be negative")

    months = years * 12
    monthly_rate = expected_annual_return / 100.0 / 12.0

    if monthly_rate == 0:
        monthly_investment = goal_amount / months
    else:
        factor = (1.0 + monthly_rate) ** months - 1.0
        monthly_investment = goal_amount * monthly_rate / factor

    total_invested = round(monthly_investment * months, 2)
    expected_growth = round(goal_amount - total_invested, 2)

    return {
        "required_monthly_investment": round(monthly_investment, 2),
        "total_invested": total_invested,
        "expected_growth": expected_growth,
    }
