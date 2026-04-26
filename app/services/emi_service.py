def calculate_emi(loan_amount: float, annual_rate: float, years: int) -> dict[str, float]:
    months = years * 12
    monthly_rate = annual_rate / 100 / 12

    if monthly_rate == 0:
        emi = loan_amount / months
    else:
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)

    total_payment = emi * months
    total_interest = total_payment - loan_amount
    return {
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2),
    }
