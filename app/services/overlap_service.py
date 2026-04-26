import re

SAFE_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9 .&'-]")


def normalize_stock_list(raw_text: str) -> list[str]:
    values = re.split(r"[\n,]+", raw_text)
    cleaned_values = (SAFE_NAME_PATTERN.sub("", value).strip().casefold() for value in values)
    return sorted({value for value in cleaned_values if value})


def calculate_overlap(first_portfolio: str, second_portfolio: str) -> dict[str, object]:
    first = set(normalize_stock_list(first_portfolio))
    second = set(normalize_stock_list(second_portfolio))
    common = sorted(first.intersection(second))
    base_count = max(len(first.union(second)), 1)
    overlap_percentage = (len(common) / base_count) * 100

    return {
        "first_count": len(first),
        "second_count": len(second),
        "common": common,
        "overlap_percentage": round(overlap_percentage, 2),
    }
