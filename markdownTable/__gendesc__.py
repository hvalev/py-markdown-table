from __init__ import markdownTable

params = [
    {'param': 'row_sep', 'type': 'str', 'values': '', 'description': 'Row separation strategy using `----` as pattern'},
    {'param': '', 'type': '', 'values': 'always', 'description': 'Separate each row'},
    {'param': '', 'type': '', 'values': 'topbottom', 'description': 'Separate the top (header) and bottom (last row) of the table'},
    {'param': '', 'type': '', 'values': 'markdown', 'description': 'Separate only header from body'},
    {'param': '', 'type': '', 'values': 'None', 'description': 'No row separators will be inserted'},
    {'param': 'padding_width', 'type': 'int', 'values': '', 'description': 'Allocate padding to all table cells'},
    {'param': 'padding_weight', 'type': 'str', 'values': '', 'description': 'Strategy for allocating padding within table cells'},
    {'param': '', 'type': '', 'values': 'left', 'description': 'Aligns cell\'s contents to the end of the cell'},
    {'param': '', 'type': '', 'values': 'right', 'description': 'Aligns cell\'s contents to the beginning of the cell'},
    {'param': '', 'type': '', 'values': 'centerleft', 'description': 'Centers cell\'s contents with extra padding allocated to the beginning of the cell'},
    {'param': '', 'type': '', 'values': 'centerright', 'description': 'Centers cell\'s contents with extra padding allocated to the end of the cell'},
    {'param': 'padding_char', 'type': 'str', 'values': '', 'description': 'Single character used to fill extra and normal padding with. Default is a blank space ` `.'},
    {'param': 'newline_char', 'type': 'str', 'values': '', 'description': 'Custom character appended to each row to force a newline. Default is `\\n`'},
    {'param': 'float_rounding', 'type': 'int', 'values': '', 'description': 'Keep values up until `float_rounder` after the decimal dot. Default is `2`, but can also be set to `None` to not round down floats.'},
    {'param': 'quote', 'type': 'bool', 'values': '', 'description': 'If `true` (default) wrap the generated markdown table with block code quote'},
    {'param': 'multiline', 'type': 'dict<Any,int>', 'values': '', 'description': 'Predefine the column width by passing a dict() with keys matching those of the passed data and values -- the desired width for each corresponding column.'},
]

widths = {'param': 17, 'type': 17, 'values': 15, 'description': 60}

print(markdownTable(params).setParams(padding_char=' ', padding_weight='centerleft', padding_width=3, row_sep='markdown', multiline=widths).getMarkdown())
