CESS_RATE = 0.04


OLD_SLABS = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]

NEW_SLABS_FY_2025_26 = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]


def _slab_tax(taxable_income: float, slabs: list[tuple[float, float]]) -> float:
    tax = 0.0
    lower = 0.0
    for upper, rate in slabs:
        if taxable_income <= lower:
            break
        amount_in_slab = min(taxable_income, upper) - lower
        tax += amount_in_slab * rate
        lower = upper
    return tax


def calculate_income_tax(
    gross_income: float,
    regime: str,
    deductions: float = 0,
    standard_deduction: float = 75000,
) -> dict[str, float | str]:
    if regime == "old":
        taxable_income = max(gross_income - deductions - 50000, 0)
        base_tax = _slab_tax(taxable_income, OLD_SLABS)
        rebate_limit = 500000
    else:
        taxable_income = max(gross_income - standard_deduction, 0)
        base_tax = _slab_tax(taxable_income, NEW_SLABS_FY_2025_26)
        rebate_limit = 1200000

    # Simple resident-individual rebate handling for calculator use.
    if taxable_income <= rebate_limit:
        base_tax = 0.0

    cess = base_tax * CESS_RATE
    total_tax = base_tax + cess
    return {
        "regime": "Old Regime" if regime == "old" else "New Regime",
        "taxable_income": round(taxable_income, 2),
        "base_tax": round(base_tax, 2),
        "cess": round(cess, 2),
        "total_tax": round(total_tax, 2),
    }
