def calculate_inflation_future_value(current_amount: float, inflation_rate: float, number_of_years: int) -> dict[str, float]:
    """Calculate future value and purchasing power impact due to inflation.

    Future value (inflation): FV = A * (1 + i/100)^n

    Purchasing power impact (educational):
    - It represents how much more money you'd need in the future to have
      equivalent purchasing power to the current amount.
    """
    if number_of_years <= 0:
        raise ValueError("Number of years must be greater than 0")
    if current_amount <= 0:
        raise ValueError("Current amount must be greater than 0")

    i = inflation_rate / 100.0
    fv = current_amount * ((1 + i) ** number_of_years)

    purchasing_power_impact = fv - current_amount

    return {
        "future_value": round(fv, 2),
        "purchasing_power_impact": round(purchasing_power_impact, 2),
    }

