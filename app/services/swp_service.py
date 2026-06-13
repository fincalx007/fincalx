def calculate_swp(
    initial_corpus: float,
    monthly_withdrawal: float,
    expected_annual_return: float,
    years: int,
) -> dict[str, float]:
    """Simulate a Systematic Withdrawal Plan (SWP).

    Assumptions:
    - Withdrawals happen monthly at the end of each month.
    - The corpus grows monthly using the expected annual return.
    - If the corpus runs out, withdrawals stop.
    """

    if years <= 0:
        raise ValueError("Duration must be greater than 0")
    if initial_corpus <= 0:
        raise ValueError("Initial corpus must be greater than 0")
    if monthly_withdrawal <= 0:
        raise ValueError("Monthly withdrawal must be greater than 0")
    if expected_annual_return < 0:
        raise ValueError("Expected annual return cannot be negative")

    months_total = years * 12
    monthly_rate = expected_annual_return / 100.0 / 12.0

    corpus = float(initial_corpus)
    total_withdrawn = 0.0

    for month_idx in range(months_total):
        # Apply monthly growth
        if monthly_rate != 0:
            corpus += corpus * monthly_rate

        # Withdraw at end of month
        withdrawal = min(monthly_withdrawal, corpus)
        corpus -= withdrawal
        total_withdrawn += withdrawal

        if corpus <= 0:
            corpus = 0.0
            break

    corpus_growth = round((corpus + total_withdrawn) - initial_corpus, 2)

    return {
        "remaining_corpus": round(corpus, 2),
        "total_withdrawals": round(total_withdrawn, 2),
        "corpus_growth": round(corpus_growth, 2),
    }
