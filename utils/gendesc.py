# pylint: skip-file
# flake8 noqa: E501
from markdownTable import markdownTable

# [monospaced fonts](https://en.wikipedia.org/wiki/Monospaced_font)
params = [
    {
        "param": "row_sep",
        "type": "str",
        "values": "",
        "description": "Row separation strategy using `----` as pattern",
    },
    {"param": "", "type": "", "values": "always", "description": "Separate each row"},
    {
        "param": "",
        "type": "",
        "values": "topbottom",
        "description": "Separate the top (header) and bottom (last row) of the table",
    },
    {
        "param": "",
        "type": "",
        "values": "markdown",
        "description": "Separate only header from body",
    },
    {
        "param": "",
        "type": "",
        "values": "None",
        "description": "No row separators will be inserted",
    },
    {
        "param": "padding_width",
        "type": "int",
        "values": "",
        "description": "Allocate padding to all table cells",
    },
    {
        "param": "padding_weight",
        "type": "str",
        "values": "",
        "description": "Strategy for allocating padding within table cells",
    },
    {
        "param": "",
        "type": "",
        "values": "left",
        "description": "Aligns the cell's contents to the end of the cell",
    },
    {
        "param": "",
        "type": "",
        "values": "right",
        "description": "Aligns the cell's contents to the beginning of the cell",
    },
    {
        "param": "",
        "type": "",
        "values": "centerleft",
        "description": "Centers cell's contents with extra padding allocated to the beginning of the cell",
    },
    {
        "param": "",
        "type": "",
        "values": "centerright",
        "description": "Centers cell's contents with extra padding allocated to the end of the cell",
    },
    {
        "param": "padding_char",
        "type": "str",
        "values": "",
        "description": "Single character used to fill padding with. Default is a blank space ` `.",
    },
    {
        "param": "newline_char",
        "type": "str",
        "values": "",
        "description": "Character appended to each row to force a newline. Default is `\\n`",
    },
    {
        "param": "float_rounding",
        "type": "int",
        "values": "",
        "description": "Integer denoting the precision of cells of `floats` after the decimal point. Default is `None`.",
    },
    {
        "param": "emoji_spacing",
        "type": "str",
        "values": "",
        "description": "Strategy for rendering emojis in tables. Currently only `mono` is supported for monospaced fonts. Default is `None` which disables special handling of emojis.",
    },
    {
        "param": "multiline",
        "type": "dict<Any,int>",
        "values": "",
        "description": "Renders the table with predefined widths by passing a `dict` with `keys` being the column names (e.g. equivalent to those in the passed `data` variable) and `values` -- the `width` of each column as an integer. Note that the width of a column cannot be smaller than the longest contiguous string present in the data.",
    },
    {
        "param": "multiline_strategy",
        "type": "str",
        "values": "",
        "description": "Strategy applied to rendering contents in multiple lines. Possible values are `rows`, `header` or `rows_and_header`. The default value is `rows`.",
    },
    {
        "param": "",
        "type": "",
        "values": "rows",
        "description": "Splits only rows overfilling by the predefined column width as provided in the `multiline` variable",
    },
    {
        "param": "",
        "type": "",
        "values": "header",
        "description": "Splits only the header overfilling by the predefined column width as provided in the `multiline` variable",
    },
    {
        "param": "",
        "type": "",
        "values": "rows_and_header",
        "description": "Splits rows and header overfilling by the predefined column width as provided in the `multiline` variable",
    },
    {
        "param": "multiline_delimiter",
        "type": "str",
        "values": "",
        "description": "Character that will be used to split a cell's contents into multiple rows. The default value is a blank space ` `.",
    },
    {
        "param": "quote",
        "type": "bool",
        "values": "",
        "description": "Wraps the generated markdown table in block quotes ```table```. Default is `True`.",
    },
]


widths = {"param": 19, "type": 17, "values": 15, "description": 28}

print(
    markdownTable(params)
    .setParams(
        padding_char=" ",
        padding_weight="centerleft",
        padding_width=2,
        row_sep="always",
        multiline=widths,
    )
    .getMarkdown()
)
