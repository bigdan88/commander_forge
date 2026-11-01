import commander_forge


def test_version() -> None:
    assert commander_forge.__version__ == "0.1.0"


def test_hello() -> None:
    assert commander_forge.hello() == "Hello from commander_forge"
