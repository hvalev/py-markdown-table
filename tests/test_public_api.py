"""What `import py_markdown_table` has to expose."""

import py_markdown_table
from py_markdown_table import MarkdownTable, markdown_table
from py_markdown_table.markdown_table import markdown_table as from_module


def test_package_level_name_is_the_class_not_the_module():
    assert callable(markdown_table)
    assert markdown_table is from_module
    assert markdown_table is MarkdownTable


def test_declared_exports_match():
    assert set(py_markdown_table.__all__) == {"markdown_table", "MarkdownTable"}
