def calculate_sip(monthly_investment: float, annual_rate: float, years: int) -> dict[str, float]:
    months = years * 12
    monthly_rate = annual_rate / 100 / 12
    total_invested = monthly_investment * months

    if monthly_rate == 0:
        maturity_amount = total_invested
    else:
        maturity_amount = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)

    returns = maturity_amount - total_invested
    return {
        "maturity_amount": round(maturity_amount, 2),
        "total_invested": round(total_invested, 2),
        "returns": round(returns, 2),
    }
