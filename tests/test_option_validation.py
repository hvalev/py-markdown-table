"""Option values must fail loudly and name the offending value."""

import pytest

from py_markdown_table import markdown_table

DATA = [{"col": "x", "other": "y"}]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"padding_width": {"typo": 5}}, id="unknown-padding_width"),
        pytest.param({"padding_weight": {"typo": "left"}}, id="unknown-padding_weight"),
        pytest.param({"multiline": {"typo": 10}}, id="unknown-multiline"),
    ],
)
def test_unknown_column_key_names_the_key(params):
    with pytest.raises(ValueError, match="typo"):
        markdown_table(DATA).set_params(**params)


@pytest.mark.parametrize("name, value", [("padding_width", 5), ("padding_weight", "left"), ("multiline", 5)])
def test_partial_column_dict_is_rejected(name, value):
    with pytest.raises(ValueError, match="other"):
        markdown_table(DATA).set_params(**{name: {"col": value}})


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"padding_char": {"col": "."}}, id="dict-padding_char"),
        pytest.param({"padding_char": ".."}, id="two-chars"),
        pytest.param({"row_sep": "sometimes"}, id="unknown-row_sep"),
        pytest.param({"padding_weight": {"col": "middle"}}, id="unknown-padding_weight"),
        pytest.param({"emoji_spacing": "wide"}, id="unknown-emoji_spacing"),
        pytest.param({"multiline_strategy": "columns"}, id="unknown-multiline_strategy"),
        pytest.param({"float_rounding": -1}, id="negative-float_rounding"),
    ],
)
def test_invalid_option_value_is_rejected(params):
    with pytest.raises(ValueError):
        markdown_table(DATA).set_params(**params)


def test_a_word_wider_than_the_column_is_rejected():
    with pytest.raises(ValueError, match="longer than the allocated column width"):
        markdown_table([{"col": "supercalifragilisticexpialidocious"}]).set_params(multiline={"col": 5})
