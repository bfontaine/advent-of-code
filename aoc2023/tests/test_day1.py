import pytest

from day01 import get_line_calibration_value


@pytest.mark.parametrize("line,p,expected", [
    ("23", 1, 23),
    ("23", 2, 23),
    ("1two", 1, 11),
    ("1two", 2, 12),
    ("twone", 2, 21),
])
def test_get_line_calibration_value(line, p, expected):
    assert get_line_calibration_value(line, p=p) == expected
