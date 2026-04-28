CESS_RATE = 0.04

OLD_SLABS = [(250000, 0.00), (500000, 0.05), (1000000, 0.20), (float("inf"), 0.30)]

# WIDENED SLABS FOR FY 2025-26
NEW_SLABS = [
    (400000, 0.00), (800000, 0.05), (1200000, 0.10), 
    (1600000, 0.15), (2000000, 0.20), (2400000, 0.25), (float("inf"), 0.30)
]

def calculate_income_tax(gross_income: float, regime: str, deductions: float = 0):
    if regime == "old":
        taxable_income = max(gross_income - deductions - 50000, 0)
        base_tax = _slab_tax(taxable_income, OLD_SLABS)
        # Rebate for Old Regime (Income up to 5L)
        if taxable_income <= 500000: base_tax = 0
    else:
        # Standard Deduction is 75,000 for New Regime
        taxable_income = max(gross_income - 75000, 0)
        base_tax = _slab_tax(taxable_income, NEW_SLABS)
        
        # Section 87A Rebate for New Regime (Income up to 12L)
        if taxable_income <= 1200000:
            base_tax = 0.0
        # Marginal Relief for New Regime (Critical for 2025 Budget)
        elif taxable_income > 1200000:
            actual_tax = base_tax
            excess_over_12L = taxable_income - 1200000
            # Tax cannot exceed the income earned above the 12L limit
            base_tax = min(actual_tax, excess_over_12L)

    cess = base_tax * CESS_RATE
    return {
        "regime": "Old" if regime == "old" else "New",
        "taxable_income": round(taxable_income, 2),
        "base_tax": round(base_tax, 2),
        "cess": round(cess, 2),
        "total_tax": round(base_tax + cess, 2),
    }

def _slab_tax(income, slabs):
    tax, lower = 0.0, 0.0
    for upper, rate in slabs:
        if income <= lower: break
        tax += (min(income, upper) - lower) * rate
        lower = upper
    return tax