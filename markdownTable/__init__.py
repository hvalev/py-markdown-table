import warnings
from py_markdown_table.markdown_table import markdown_table


class markdownTable(markdown_table):
    def __init__(self, data):
        warnings.warn(
            "This constructor will be deprecated soon. \
                Please use `from py_markdown_table.markdown_table import import markdown_table` to import. \
                To initialize a markdownTable() object use the `markdown_table()` constructor instead",
            DeprecationWarning,
        )
        super().__init__(data)
