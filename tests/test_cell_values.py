"""Any value type a caller can put in a dict must survive every render mode."""

import pytest

from py_markdown_table import markdown_table

VALUES = [7, 7.5, None, True, 0, [1, 2]]


@pytest.mark.parametrize("value", VALUES)
def test_plain_rendering(value):
    assert str(value) in markdown_table([{"n": value}]).get_markdown()


@pytest.mark.parametrize("value", VALUES)
def test_multiline_rendering(value):
    """This used to fail with AttributeError: no 'split' on int."""
    out = markdown_table([{"n": value}]).set_params(multiline={"n": 20}).get_markdown()
    assert str(value) in out


@pytest.mark.parametrize("value", VALUES)
def test_emoji_spacing_rendering(value):
    """This used to fail with TypeError in count_emojis()."""
    out = markdown_table([{"n": value}]).set_params(emoji_spacing="mono").get_markdown()
    assert str(value) in out


def test_floats_round_without_touching_the_source_rows():
    data = [{"v": 1.2349}]
    out = markdown_table(data).set_params(float_rounding=2).get_markdown()
    assert "1.23" in out
    assert data == [{"v": 1.2349}]


def test_markdown_syntax_is_not_stripped_when_validation_is_skipped():
    cell = "a [link](http://example.com) and `code`"
    out = markdown_table([{"md": cell}], skip_data_validation=True).get_markdown()
    assert cell in out
