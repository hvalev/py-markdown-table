"""Wrapping has to honour the requested width without editing the content."""

import pytest

from py_markdown_table import markdown_table

WIDE = "row1_A and additional stuff"


def test_padding_does_not_eat_the_content_width():
    """`multiline` is the content width, so padding must not change the wrap.

    A 27 character line in a column asked to hold 25 has to wrap whether the
    padding is 0 or 2; it used to only wrap at padding_width=0, because the
    comparison was made against the whole column width.
    """
    short = markdown_table([{"col": WIDE}]).set_params(multiline={"col": 25}, padding_width=0).get_markdown()
    padded = markdown_table([{"col": WIDE}]).set_params(multiline={"col": 25}, padding_width=2).get_markdown()
    assert len(short.split("\n")) == len(padded.split("\n"))
    assert "additional stuff" not in short
    assert "additional stuff" not in padded


@pytest.mark.parametrize("emoji_spacing", [None, "mono"], ids=["off", "mono"])
def test_wrapping_does_not_insert_characters(emoji_spacing):
    """Re-joining a wrapped line used to use the delimiter, so an emoji inside
    a word grew spaces."""
    cell = "hello a\U0001f600b world"
    out = markdown_table([{"col": cell}]).set_params(multiline={"col": 6}, emoji_spacing=emoji_spacing).get_markdown()
    assert "a\U0001f600b" in out.replace(" ", "").replace("|", "").replace("\n", "")


@pytest.mark.parametrize("emoji_spacing", [None, "mono"], ids=["off", "mono"])
def test_every_value_survives_wrapping(emoji_spacing):
    """Whatever the wrapping does, the characters of the input stay together."""
    data = [{"col": "one two three", "other": "x\U0001f389y and more words here"}]
    out = markdown_table(data).set_params(multiline={"col": 5, "other": 6}, emoji_spacing=emoji_spacing).get_markdown()
    for row in data:
        for value in row.values():
            for word in value.replace("\U0001f389", " \U0001f389 ").split():
                assert word in out


def test_a_run_of_emoji_wraps_instead_of_overflowing():
    """Emoji are break opportunities, so a run wider than the column is legal."""
    out = markdown_table([{"col": "\U0001f60a\U0001f30d\U0001f389"}]).set_params(
        multiline={"col": 5}, emoji_spacing="mono"
    ).get_markdown()
    assert "```" in out


def test_custom_delimiter_is_used_when_rejoining():
    out = markdown_table([{"col": "aa,bb,cc,dd"}]).set_params(
        multiline={"col": 5}, multiline_delimiter=","
    ).get_markdown()
    assert "aa,bb" in out
    assert "aa bb" not in out


def test_a_word_that_cannot_fit_is_reported_not_hung_on():
    """An unbreakable word wider than the column used to leave the wrapping
    loop reconsidering the same piece forever."""
    with pytest.raises(ValueError, match="longer than the allocated column width"):
        markdown_table([{"col": "ab cdefghijkl"}]).set_params(multiline={"col": 3})
