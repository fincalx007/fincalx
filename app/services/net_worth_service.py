def calculate_net_worth(total_assets: float, total_liabilities: float) -> dict[str, float]:
    """Compute net worth.

    Net worth = total assets - total liabilities
    """
    if total_assets < 0:
        raise ValueError("Total assets must be non-negative")
    if total_liabilities < 0:
        raise ValueError("Total liabilities must be non-negative")

    net_worth = total_assets - total_liabilities

    return {"net_worth": round(net_worth, 2)}

