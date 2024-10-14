from hadoop.social_media_connect.mapper import mapper


def test_mapper() -> None:
    lines = [
        "A\tB",
        "A\tC",
        "A\tD",
    ]

    expectd = [
        ("B", "C"),
        ("C", "B"),
        ("B", "D"),
        ("D", "B"),
        ("C", "D"),
        ("D", "C"),
    ]

    actual = list(mapper(lines))
    assert expectd == actual
