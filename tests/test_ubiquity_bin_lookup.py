import pytest

from shared_config_storage.ubiquity import bin_lookup


@pytest.mark.parametrize(
    "first_six,expected",
    [
        ("100000", "other"),
        ("200000", "other"),
        ("222100", "mastercard"),
        ("272000", "mastercard"),
        ("340000", "amex"),
        ("370000", "amex"),
        ("400000", "visa"),
        ("410000", "visa"),
        ("510000", "mastercard"),
        ("550000", "mastercard"),
        ("600000", "other"),
    ],
)
def test_card_bin_lookup(first_six, expected):
    result = bin_lookup.bin_to_provider(first_six)

    assert result == expected
