"""Test to suppress coverage warnings about empty directory."""


def test_import():
    import orchestrator.handler  # noqa: F401
