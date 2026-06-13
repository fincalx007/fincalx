def calculate_compound_interest(principal_amount: float, interest_rate: float, time_period_years: int, compounding_frequency: int) -> dict[str, float]:
    """Calculate compound interest.

    A = P * (1 + r/n)^(n*t)
    Interest earned = A - P

    - P: principal
    - r: annual interest rate (percent)
    - n: compounding frequency per year
    - t: time in years
    """
    if time_period_years <= 0:
        raise ValueError("Time period must be greater than 0")
    if principal_amount <= 0:
        raise ValueError("Principal amount must be greater than 0")
    if compounding_frequency <= 0:
        raise ValueError("Compounding frequency must be greater than 0")

    r = interest_rate / 100.0
    n = compounding_frequency
    t = time_period_years

    maturity = principal_amount * ((1 + r / n) ** (n * t))
    interest_earned = maturity - principal_amount

    return {
        "interest_earned": round(interest_earned, 2),
        "maturity_value": round(maturity, 2),
    }

