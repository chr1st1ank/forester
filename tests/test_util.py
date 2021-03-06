import pytest

from forester import util


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("some string", "some string"),
        (12345, "12,345"),
        (12345678, "12,345,678"),
        (1234.5, "1,234.5"),
        (150, "150"),
    ],
)
def test_format_number(input, expected_output):
    """Test the number formatting"""
    assert util.format_number(input) == expected_output


def test_format_timestamp():
    """Test date formatting"""
    assert util.format_timestamp(1578096397) == "2020-01-04 00:06:37"


def test_format_timestamp_error():
    """Test handling of invalid input. Should be returned as string only."""
    assert util.format_timestamp("abc") == "abc"


@pytest.mark.parametrize(
    "text, length, expected_output",
    [
        ("abcdefg", 8, "abcdefg"),
        ("abcdefg", 7, "abcdefg"),
        ("abcdefg", 6, "abc..."),
    ],
)
def test_cut_to_length(text, length, expected_output):
    """Test the cut_to_length function"""
    assert util.cut_to_length(text, length) == expected_output
