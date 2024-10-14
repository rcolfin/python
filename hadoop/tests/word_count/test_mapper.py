from hadoop.word_count.mapper import mapper


def test_mapper() -> None:
    lines = ["A B C C"]
    expected = [
        ("A", 1),
        ("B", 1),
        ("C", 1),
        ("C", 1),
    ]

    actual = list(mapper(lines))
    assert expected == actual
