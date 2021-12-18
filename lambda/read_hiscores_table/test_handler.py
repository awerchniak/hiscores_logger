import importlib
import pytest


@pytest.fixture
def queryer_handler(monkeypatch):
    """Import within a fixture so we can set environment variables."""
    monkeypatch.setenv("HISCORES_TABLE_NAME", "hiscores-table-name")
    module = importlib.import_module("read_hiscores_table.handler")
    return module


def test_handler(queryer_handler):
    print(type(queryer_handler))
