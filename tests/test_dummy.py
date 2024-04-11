# test_dummy.py
from __future__ import annotations


def test_addition():
    """Test addition operation."""
    assert 1 + 1 == 2


def test_subtraction():
    """Test subtraction operation."""
    assert 3 - 1 == 2


def test_multiplication():
    """Test multiplication operation."""
    assert 2 * 3 == 6


def test_division():
    """Test division operation."""
    assert 6 / 2 == 3


def test_string_concatenation():
    """Test string concatenation."""
    assert "Hello, " + "world!" == "Hello, world!"


def test_list_concatenation():
    """Test list concatenation."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    assert list1 + list2 == [1, 2, 3, 4, 5, 6]


def test_dictionary():
    """Test dictionary functionality."""
    my_dict = {"key": "value"}
    assert my_dict["key"] == "value"


def test_boolean():
    """Test boolean operation."""
    assert True is True


def test_membership():
    """Test membership."""
    my_list = [1, 2, 3, 4, 5]
    assert 3 in my_list


def test_exception():
    """Test handling of exception."""
    try:
        1 / 0
    except ZeroDivisionError:
        assert True
    else:
        assert False, "Expected ZeroDivisionError but none was raised"
