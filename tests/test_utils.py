"""The helpers in `py_markdown_table.utils` are public and usable on their own."""

import pytest

from py_markdown_table.utils import (
    count_emojis,
    find_longest_contiguous_strings,
    split_list_by_indices,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", []),
        ("plain text", []),
        ("a\U0001f600b", [(1, "\U0001f600")]),
        ("\U0001f60a\U0001f30d\U0001f389", [(0, "\U0001f60a"), (1, "\U0001f30d"), (2, "\U0001f389")]),
        ("\U0001f600 \U0001f600", [(0, "\U0001f600"), (2, "\U0001f600")]),
    ],
)
def test_count_emojis(text, expected):
    assert [(entry["index"], entry["value"]) for entry in count_emojis(text)] == expected


def test_find_longest_contiguous_strings_ignores_the_delimiter():
    assert find_longest_contiguous_strings([{"col": "aaa bb cccc"}]) == {"col": 4}
    assert find_longest_contiguous_strings([{"col": "aa,bbbbb"}], delimiter=",") == {"col": 5}


def test_find_longest_contiguous_strings_can_include_the_header():
    data = [{"verylongkey": "ab"}]
    assert find_longest_contiguous_strings(data) == {"verylongkey": 2}
    assert find_longest_contiguous_strings(data, include_header=True) == {"verylongkey": 11}


def test_find_longest_contiguous_strings_takes_the_longest_over_all_rows():
    data = [{"col": "short"}, {"col": "much longer"}, {"col": "ti"}]
    assert find_longest_contiguous_strings(data) == {"col": 6}


@pytest.mark.parametrize(
    ("text", "indices", "expected"),
    [(("abcdef"), [2, 4], ["ab", "cd", "ef"]), ("abc", [], ["abc"]), ("abc", [0], ["", "abc"])],
)
def test_split_list_by_indices(text, indices, expected):
    assert split_list_by_indices(text, indices) == expected


def test_characters_that_are_not_wide_are_not_counted():
    """The previous implementation carried its own table of code point ranges
    and treated arrows, stars and check marks as two columns wide."""
    assert count_emojis("a→b★c✓d☀e") == []
    assert count_emojis("© ü 1") == []


def test_wide_characters_outside_the_emoji_blocks_are_counted():
    """CJK is two columns wide in a monospaced font too, and was missed."""
    assert [entry["value"] for entry in count_emojis("日本語")] == ["日", "本", "語"]


def test_a_variation_selector_widens_the_character_before_it():
    """U+FE0F asks for emoji presentation; the selector itself takes no room."""
    hearts = count_emojis("❤️ ok")
    assert [entry["index"] for entry in hearts] == [0]
