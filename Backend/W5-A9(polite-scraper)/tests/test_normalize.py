import pytest
from src.normalize import normalize_price


def test_normalize_price_basic():
    assert normalize_price("£51.77") == 51.77


def test_normalize_price_with_comma_thousands():
    assert normalize_price("£1,234.50") == 1234.50


def test_normalize_price_empty_raises():
    with pytest.raises(ValueError):
        normalize_price("")


def test_normalize_price_malformed_raises():
    with pytest.raises(ValueError):
        normalize_price("price unavailable")
