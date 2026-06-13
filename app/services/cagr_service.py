def calculate_cagr(initial_investment: float, final_value: float, years: int) -> dict[str, float]:
    """Calculate CAGR.

    CAGR = ((Final / Initial)^(1 / Years) - 1) * 100
    """
    if years <= 0:
        raise ValueError("Years must be greater than 0")
    if initial_investment <= 0:
        raise ValueError("Initial investment must be greater than 0")

    ratio = final_value / initial_investment
    if ratio <= 0:
        # CAGR with non-positive values is not well-defined for this calculator.
        raise ValueError("Values must result in a positive growth ratio")

    cagr = (ratio ** (1 / years) - 1) * 100
    return {"cagr": round(cagr, 4)}

