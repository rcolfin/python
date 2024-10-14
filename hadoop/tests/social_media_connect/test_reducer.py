from hadoop.social_media_connect.reducer import reducer


def test_reducer() -> None:
    lines = [
        "B\tC",
        "C\tB",
        "B\tD",
        "D\tB",
        "C\tD",
        "D\tC",
    ]

    expected = [
        ("B", ("C", "D")),
        ("C", ("B", "D")),
        ("D", ("B", "C")),
    ]

    actual = list(reducer(lines))
    assert expected == actual
