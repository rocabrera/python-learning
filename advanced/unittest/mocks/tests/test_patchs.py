import src.example.patchs as f
from unittest.mock import patch

@patch("src.example.patchs.requests")
def test_call_api(mock_request):
    result = f.call_api("user", "password")
    assert True

@patch("src.example.patchs.open")
def test_read_file(mock_open):
    mock_open.read.return_value = "teste"
    info = f.read_file("teste")
    assert True