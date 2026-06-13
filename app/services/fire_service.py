def calculate_fire(annual_expenses: float, safe_withdrawal_rate: float) -> dict[str, float]:
    """Calculate FIRE number and required retirement corpus.

    FIRE number = annual_expenses / (safe_withdrawal_rate / 100)
    """

    if annual_expenses < 0:
        raise ValueError("Annual expenses cannot be negative")
    if safe_withdrawal_rate <= 0:
        raise ValueError("Safe withdrawal rate must be greater than 0")

    corpus = annual_expenses / (safe_withdrawal_rate / 100.0)

    return {
        "fire_number": round(corpus, 2),
        "required_retirement_corpus": round(corpus, 2),
    }
