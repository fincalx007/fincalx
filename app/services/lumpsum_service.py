from dataclasses import dataclass


def calculate_lumpsum(investment_amount: float, expected_annual_return: float, investment_duration_years: int) -> dict[str, float]:
    """Calculate maturity value and estimated returns for a lumpsum investment.

    Future value (lumpsum) = P * (1 + r/100) ^ n
    Estimated returns = FV - P
    """
    if investment_duration_years <= 0:
        raise ValueError("Investment duration must be greater than 0")
    if investment_amount <= 0:
        raise ValueError("Investment amount must be greater than 0")

    r = expected_annual_return / 100.0
    fv = investment_amount * ((1 + r) ** investment_duration_years)
    returns = fv - investment_amount

    return {
        "invested_amount": round(investment_amount, 2),
        "estimated_returns": round(returns, 2),
        "maturity_value": round(fv, 2),
    }

