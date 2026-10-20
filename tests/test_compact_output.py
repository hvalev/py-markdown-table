"""`compact` emits the smallest table that is still valid markdown."""

import pytest

from py_markdown_table import markdown_table

DATA = [
    {
        "_time": "2025-10-03T12:54:42.000+00:00",
        "field1": "text text",
        "field2": "aa bb cc",
        "field3": "texttexttext--aaa",
        "field4": "1112223344",
    }
]


def test_no_duplicated_spaces_or_dashes():
    """The output a caller with a character budget asked for in #24."""
    out = markdown_table(DATA).set_params(row_sep="markdown", quote=False, compact=True).get_markdown()
    assert out == (
        "|_time|field1|field2|field3|field4|\n"
        "|-|-|-|-|-|\n"
        "|2025-10-03T12:54:42.000+00:00|text text|aa bb cc|texttexttext--aaa|1112223344|"
    )


def test_compact_still_quotes_unless_asked_not_to():
    out = markdown_table(DATA).set_params(row_sep="markdown", compact=True).get_markdown()
    assert out.startswith("```|_time|")
    assert out.endswith("|```")


@pytest.mark.parametrize("row_sep", ["always", "topbottom", None])
def test_compact_needs_a_renderer_to_draw_the_borders(row_sep):
    with pytest.raises(ValueError, match="requires row_sep 'markdown'"):
        markdown_table(DATA).set_params(row_sep=row_sep, compact=True)


def test_compact_rejects_a_non_boolean():
    with pytest.raises(ValueError, match="compact value"):
        markdown_table(DATA).set_params(row_sep="markdown", compact="yes")


def test_compact_keeps_multiline_widths_without_padding_them_out():
    """Wrapping is still useful in compact output; padding is not."""
    data = [{"col": "one two three four five six"}]
    out = markdown_table(
        data
    ).set_params(row_sep="markdown", quote=False, compact=True, multiline={"col": 9}, padding_width=4).get_markdown()
    assert out == "|col|\n|-|\n|one two|\n|three|\n|four five|\n|six|"


def test_compact_output_has_no_padding_characters():
    out = markdown_table(DATA).set_params(row_sep="markdown", quote=False, compact=True).get_markdown()
    for line in out.split("\n"):
        cell = line.strip("|")
        assert not cell.startswith(" ")
        assert not cell.endswith(" ")
