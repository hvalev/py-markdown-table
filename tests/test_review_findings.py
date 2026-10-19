"""Tests for the defects fixed after a code review of the rendering path."""

import pytest

from py_markdown_table import MarkdownTable, markdown_table
from py_markdown_table.utils import find_longest_contiguous_strings

LONG = "aaa bbb ccc ddd eee"


def test_rendering_is_idempotent():
    """A second render must not widen the table (padding used to accumulate)."""
    mt = markdown_table([{"col": LONG}]).set_params(multiline={"col": 12}, padding_width=3)
    assert mt.get_markdown() == mt.get_markdown()


def test_set_params_does_not_mutate_the_callers_multiline_dict():
    widths = {"col": 12}
    mt = markdown_table([{"col": LONG}]).set_params(multiline=widths, padding_width=3)
    assert widths == {"col": 12}
    mt.get_markdown()
    assert widths == {"col": 12}


def test_set_params_does_not_mutate_the_callers_padding_dicts():
    widths = {"col": 2}
    weights = {"col": "left"}
    markdown_table([{"col": LONG}]).set_params(padding_width=widths, padding_weight=weights)
    assert widths == {"col": 2}
    assert weights == {"col": "left"}


def test_float_rounding_does_not_mutate_the_input_rows():
    data = [{"v": 1.2349}]
    out = markdown_table(data).set_params(float_rounding=2).get_markdown()
    assert "1.23" in out
    assert data == [{"v": 1.2349}]


@pytest.mark.parametrize("value", [7, 7.5, None, True])
def test_non_string_cells_render(value):
    out = markdown_table([{"n": value}]).get_markdown()
    assert str(value) in out


@pytest.mark.parametrize("value", [7, 7.5, None])
def test_non_string_cells_work_with_multiline(value):
    """multiline used to call .split() on the raw value and raise."""
    out = markdown_table([{"n": value}]).set_params(multiline={"n": 20}).get_markdown()
    assert str(value) in out


@pytest.mark.parametrize("value", [7, 7.5, None])
def test_non_string_cells_work_with_emoji_spacing(value):
    """count_emojis used to be handed the raw value and raise."""
    out = markdown_table([{"n": value}]).set_params(emoji_spacing="mono").get_markdown()
    assert str(value) in out


@pytest.mark.parametrize(
    "params",
    [
        {"padding_width": {"typo": 5}},
        {"padding_weight": {"typo": "left"}},
        {"multiline": {"typo": 10}},
    ],
)
def test_unknown_column_key_is_reported_by_name(params):
    with pytest.raises(ValueError, match="typo"):
        markdown_table([{"col": "x"}]).set_params(**params)


def test_missing_column_key_is_reported():
    with pytest.raises(ValueError, match="other"):
        markdown_table([{"col": "x", "other": "y"}]).set_params(padding_width={"col": 5})


def test_padding_char_rejects_a_dict():
    with pytest.raises(ValueError):
        markdown_table([{"col": "x"}]).set_params(padding_char={"col": "."})


def test_reconfiguration_replaces_instead_of_accumulating():
    mt = markdown_table([{"col": LONG}])
    first = mt.set_params(multiline={"col": 12}, padding_width=3).get_markdown()
    again = mt.set_params(multiline={"col": 12}, padding_width=3).get_markdown()
    assert first == again


def test_package_level_export_is_the_class():
    assert markdown_table is MarkdownTable
    assert callable(markdown_table)


def test_find_longest_contiguous_strings_is_usable():
    data = [{"col": "aaa bb cccc"}]
    assert find_longest_contiguous_strings(data) == {"col": 4}
    assert find_longest_contiguous_strings(data, include_header=True) == {"col": 4}
