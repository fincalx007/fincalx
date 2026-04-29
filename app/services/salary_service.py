def calculate_salary(
    ctc: float,
    basic_pct: float,
    hra_pct: float,
    other_allowances: float,
    pf_pct: float,
    tax_pct: float,
) -> dict[str, float]:
    """Calculate salary breakdown from CTC using simplified assumptions."""
    basic = ctc * (basic_pct / 100)
    hra = basic * (hra_pct / 100)
    pf = basic * (pf_pct / 100)
    tax = ctc * (tax_pct / 100)
    total_deductions = pf + tax
    in_hand = ctc - total_deductions
    monthly = in_hand / 12

    return {
        "basic": round(basic, 2),
        "hra": round(hra, 2),
        "other_allowances": round(other_allowances, 2),
        "pf": round(pf, 2),
        "tax": round(tax, 2),
        "total_deductions": round(total_deductions, 2),
        "in_hand": round(in_hand, 2),
        "monthly": round(monthly, 2),
    }

