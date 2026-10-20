"""What `import py_markdown_table` has to expose."""

import inspect
import pathlib
import re

import py_markdown_table
from py_markdown_table import MarkdownTable, markdown_table
from py_markdown_table.markdown_table import markdown_table as from_module


def test_package_level_name_is_the_class_not_the_module():
    assert callable(markdown_table)
    assert markdown_table is from_module
    assert markdown_table is MarkdownTable


def test_declared_exports_match():
    assert set(py_markdown_table.__all__) == {"markdown_table", "MarkdownTable"}


def test_every_option_is_documented_in_the_readme():
    """The keyword table is generated from the docstrings, so a new option that
    skips its docstring entry would silently stay undocumented."""
    readme = (pathlib.Path(__file__).resolve().parent.parent / "README.md").read_text()
    options = [name for name in inspect.signature(markdown_table.set_params).parameters if name != "self"]
    undocumented = [name for name in options if not re.search(rf"^\|\s*{name}\s*\|", readme, re.M)]
    assert not undocumented, f"missing from the README keyword table: {undocumented}"
