"""Unit tests for command.folder_contributions"""
import pytest

from command import folder_contributions

@pytest.mark.parametrize('input, expected_output', [
    ("some string", "some string"),
    (12345, "12,345"),
    (12345678, "12,345,678"),
    (1234.5, "1,234.5"),
    (150, "150"),
])
def test_format_number(input, expected_output):
    """Test the number formatting"""
    assert folder_contributions.format_number(input) == expected_output
