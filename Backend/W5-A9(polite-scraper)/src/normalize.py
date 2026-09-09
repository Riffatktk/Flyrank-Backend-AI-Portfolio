"""Stage 4: turn raw strings into clean values a program can sort and compare."""
import re

_PRICE_RE = re.compile(r"[\d,]+\.?\d*")


def normalize_price(price_text):
    """'£51.77' -> 51.77. Raises ValueError if no number is found, so a
    malformed price fails validation instead of silently becoming 0.0."""
    if not price_text:
        raise ValueError("empty price_text")
    match = _PRICE_RE.search(price_text)
    if not match:
        raise ValueError(f"no numeric value found in price_text: {price_text!r}")
    return float(match.group().replace(",", ""))
