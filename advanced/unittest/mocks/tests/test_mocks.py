import src.example.mocks as f
from unittest.mock import MagicMock

# Simple test
def test_func1():
    x = 10
    result = f.func1(10)
    assert 20 == result

# MagicMock
def test_check_shop_list():
    mock_usr = MagicMock()
    mock_ps = MagicMock()
    f.check_shop_list(mock_usr, mock_ps)
