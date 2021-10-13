import src.example.mocks as f
from unittest.mock import MagicMock

def test_func1():
    x = 10
    result = f.func1(10)
    assert 20 == result

def test_check_shop_list():
    mock_usr = MagicMock()
    mock_ps = MagicMock()
    f.check_shop_list(mock_usr, mock_ps)

def test_check_shop_list2():
    mock_usr = MagicMock()
    mock_usr.full.return_value = False

    mock_ps = MagicMock()
    result = f.check_shop_list(mock_usr, mock_ps)
    assert True

def test_check_shop_list3():
    mock_usr = MagicMock()
    mock_usr.full.return_value = False
    mock_usr.__gt__.return_value = True
    
    mock_ps = MagicMock()
    mock_ps.qtd.return_value = False

    result = f.check_shop_list(mock_usr, mock_ps)
    assert True