def calculate_step_up_sip(
    monthly_investment: float,
    annual_step_up_percentage: float,
    expected_annual_return: float,
    years: int,
) -> dict[str, float]:
    """Calculate maturity for a Step-Up SIP.

    Assumptions (educational):
    - Step-up happens once per year on the anniversary (year 1 contribution = P,
      year 2 contribution = P*(1+step_up_rate), etc.).
    - Compounding and growth applied monthly using expected annual return.
    - Each month's contribution is treated as happening at the end of the month.
    """

    if years <= 0:
        raise ValueError("Investment duration must be greater than 0")
    if monthly_investment <= 0:
        raise ValueError("Monthly SIP amount must be greater than 0")
    if expected_annual_return < 0:
        raise ValueError("Expected annual return cannot be negative")
    if annual_step_up_percentage < 0:
        raise ValueError("Annual step-up percentage cannot be negative")

    months_total = years * 12
    monthly_rate = expected_annual_return / 100.0 / 12.0

    step_up_rate = annual_step_up_percentage / 100.0

    total_invested = 0.0
    maturity = 0.0

    for month_idx in range(months_total):
        year_idx = month_idx // 12  # 0-based
        step_multiplier = (1.0 + step_up_rate) ** year_idx
        contribution = monthly_investment * step_multiplier

        total_invested += contribution

        # Future value accumulation factor from contribution month to maturity
        months_remaining_after_this = months_total - 1 - month_idx
        if monthly_rate == 0:
            maturity += contribution
        else:
            maturity += contribution * ((1.0 + monthly_rate) ** months_remaining_after_this)

    returns = maturity - total_invested

    return {
        "total_invested": round(total_invested, 2),
        "wealth_generated": round(returns, 2),
        "maturity_value": round(maturity, 2),
    }

