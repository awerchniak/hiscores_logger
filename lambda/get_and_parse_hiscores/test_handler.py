import importlib
import pytest


@pytest.fixture
def get_and_parse_handler(monkeypatch):
    """Import within a fixture so we can set environment variables."""
    monkeypatch.setenv("HISCORES_TABLE_NAME", "hiscores-table-name")
    module = importlib.import_module("get_and_parse_hiscores.handler")
    return module


def test_handler(get_and_parse_handler):
    print(type(get_and_parse_handler))
