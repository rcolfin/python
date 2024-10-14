import pytest


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 1, 2),
    ],
)
def test_add(x: int, y: int, expected: int) -> None:
    assert x + y is expected
