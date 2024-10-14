from hadoop.word_count.reducer import reducer


def test_reducer() -> None:
    lines = ["A\t1", "A\t1", "B\t1", "C\t1"]
    expected = [
        ("A", 2),
        ("B", 1),
        ("C", 1),
    ]

    actual = list(reducer(lines))
    assert expected == actual
