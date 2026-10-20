"""Rendering must not depend on hidden state: no mutation, no accumulation.

The width pipeline used to write into the caller's data and option dicts and
then widen the columns again on every get_markdown() call, so these cases are
pinned here deliberately.
"""

from py_markdown_table import markdown_table

WRAPS_AT_25 = "row1_A and additional stuff"


def test_repeated_renders_are_identical():
    mt = markdown_table([{"col": WRAPS_AT_25}])
    mt.set_params(multiline={"col": 15}, padding_width=3)
    assert mt.get_markdown() == mt.get_markdown()


def test_reconfiguring_replaces_the_previous_options():
    mt = markdown_table([{"col": WRAPS_AT_25}])
    first = mt.set_params(multiline={"col": 15}, padding_width=3).get_markdown()
    again = mt.set_params(multiline={"col": 15}, padding_width=3).get_markdown()
    assert first == again


def test_set_params_leaves_the_multiline_dict_alone():
    widths = {"col": 15}
    markdown_table([{"col": WRAPS_AT_25}]).set_params(multiline=widths, padding_width=3)
    assert widths == {"col": 15}


def test_set_params_leaves_the_padding_dicts_alone():
    widths = {"col": 2}
    weights = {"col": "left"}
    markdown_table([{"col": WRAPS_AT_25}]).set_params(padding_width=widths, padding_weight=weights)
    assert widths == {"col": 2}
    assert weights == {"col": "left"}


def test_rendering_leaves_the_input_rows_alone():
    data = [{"col": WRAPS_AT_25}]
    snapshot = [dict(row) for row in data]
    mt = markdown_table(data).set_params(multiline={"col": 15}, padding_width=3)
    mt.get_markdown()
    mt.get_markdown()
    assert data == snapshot
