"""The one invariant that matters here: a rendered table is a rectangle.

Column width is computed in several places (header, body, separators,
multiline wrapping, emoji compensation), so a mistake shows up as a ragged
table rather than an error.

Widths are compared in terminal *display* columns, not characters: with
`emoji_spacing="mono"` a cell is deliberately written with one character per
emoji less than its column, because the emoji itself is drawn two columns
wide. A row full of emoji is therefore shorter as text and the same width on
screen.
"""

import itertools

import pytest

from py_markdown_table import markdown_table
from py_markdown_table.utils import count_emojis

DATA = [
    {"name": "widget", "qty": 3, "price": 1.5, "note": "ok"},
    {"name": "gadget plus", "qty": 12, "price": 20.25, "note": "needs a much longer cell here"},
    {"name": "doodad", "qty": 0, "price": 0.125, "note": "\U0001f389"},
    {"name": "thing", "qty": 7, "price": 9.99, "note": "\U0001f600\U0001f30d party \U0001f389"},
]

ROW_SEPS = ["always", "topbottom", "markdown"]
PADDING_WIDTHS = [0, 1, 3, 5]
PADDING_WEIGHTS = ["left", "right", "centerleft", "centerright"]


def _lines(markdown):
    """The rendered table without its code fences.

    With `row_sep="markdown"` the fences sit against the first and last line,
    otherwise they get a line of their own.
    """
    lines = markdown.split("\n")
    if lines[0] == "```":
        lines.pop(0)
    elif lines[0].startswith("```"):
        lines[0] = lines[0][len("```") :]
    if lines[-1] == "```":
        lines.pop()
    elif lines[-1].endswith("```"):
        lines[-1] = lines[-1][: -len("```")]
    return lines


def _assert_rectangular(markdown, mono=False):
    lines = _lines(markdown)
    assert lines, "nothing was rendered"
    widths = {len(line) + (len(count_emojis(line)) if mono else 0) for line in lines}
    assert len(widths) == 1, f"ragged table, display widths {sorted(widths)}\n{markdown}"
    return lines


@pytest.mark.parametrize(
    ("row_sep", "padding_width", "padding_weight"),
    list(itertools.product(ROW_SEPS, PADDING_WIDTHS, PADDING_WEIGHTS)),
    ids=lambda value: str(value),
)
def test_plain_table_is_rectangular(row_sep, padding_width, padding_weight):
    out = markdown_table(DATA).set_params(
        row_sep=row_sep, padding_width=padding_width, padding_weight=padding_weight
    ).get_markdown()
    _assert_rectangular(out)


@pytest.mark.parametrize("padding_weight", PADDING_WEIGHTS)
@pytest.mark.parametrize("width", [6, 8, 12, 30])
def test_multiline_table_is_rectangular(width, padding_weight):
    """Wrapping has to keep every produced line inside the requested width."""
    out = markdown_table(DATA).set_params(
        multiline=dict.fromkeys(DATA[0], width), padding_weight=padding_weight, padding_width=2
    ).get_markdown()
    lines = _assert_rectangular(out)
    for line in lines:
        assert len(line) <= len(lines[0]), f"a wrapped line is wider than the table:\n{out}"


@pytest.mark.parametrize("emoji_spacing", [None, "mono"], ids=["off", "mono"])
@pytest.mark.parametrize("row_sep", ROW_SEPS)
def test_emoji_table_is_rectangular(emoji_spacing, row_sep):
    out = markdown_table(DATA).set_params(emoji_spacing=emoji_spacing, row_sep=row_sep).get_markdown()
    _assert_rectangular(out, mono=emoji_spacing == "mono")


@pytest.mark.parametrize("row_sep", ROW_SEPS)
def test_no_line_ends_in_whitespace(row_sep):
    """Trailing spaces survive into markdown renderers as visible drift."""
    out = markdown_table(DATA).set_params(row_sep=row_sep, padding_width=3).get_markdown()
    offenders = [line for line in _lines(out) if line != line.rstrip()]
    assert not offenders, f"{len(offenders)} line(s) end with spaces"


@pytest.mark.parametrize("row_sep", ROW_SEPS)
def test_every_value_of_the_data_appears(row_sep):
    out = markdown_table(DATA).set_params(row_sep=row_sep).get_markdown()
    for row in DATA:
        for value in row.values():
            assert str(value) in out


@pytest.mark.parametrize("emoji_spacing", [None, "mono"], ids=["off", "mono"])
def test_wide_script_is_rectangular(emoji_spacing):
    """CJK and emoji are both two columns wide, so the same rule has to hold
    for text that is not Latin."""
    data = [{"cjk": "日本語のテキスト", "mix": "ok \U0001f600 emoji", "n": 1}, {"cjk": "한글", "mix": "plain", "n": 22}]
    out = markdown_table(data).set_params(emoji_spacing=emoji_spacing).get_markdown()
    _assert_rectangular(out, mono=emoji_spacing == "mono")
