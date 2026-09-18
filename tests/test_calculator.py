import pytest

from controllers.calculator import sum_numbers


def test_sum_positive_integers():
    assert sum_numbers(1, 2) == 3
    assert sum_numbers(10, 20) == 30


def test_sum_zero():
    assert sum_numbers(0, 0) == 0
    assert sum_numbers(5, 0) == 5
    assert sum_numbers(0, -3) == -3


def test_sum_negative():
    assert sum_numbers(-1, -2) == -3
    assert sum_numbers(10, -4) == 6


def test_sum_floats():
    assert sum_numbers(1.5, 2.5) == 4.0
    assert sum_numbers(0.1, 0.2) == pytest.approx(0.3)
    assert sum_numbers(-1.5, 3.5) == 2.0
