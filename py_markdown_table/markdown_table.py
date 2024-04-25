import math
from typing import Tuple, List, Dict
from py_markdown_table.utils import count_emojis, split_list_by_indices


class markdown_table:
    """
    A class used to generate padded tables in a markdown code block

    +--------------------------------------------------------------------------------------------------+
    |         param         |         type        |       values      |           description          |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |        row_sep        |         str         |                   |  Row separation strategy using |
    |                       |                     |                   |        `----` as pattern       |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |       always      |        Separate each row       |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |     topbottom     |  Separate the top (header) and |
    |                       |                     |                   | bottom (last row) of the table |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |      markdown     | Separate only header from body |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |        None       |    No row separators will be   |
    |                       |                     |                   |            inserted            |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |     padding_width     |         int         |                   |  Allocate padding to all table |
    |                       |                     |                   |              cells             |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |     padding_weight    |         str         |                   |     Strategy for allocating    |
    |                       |                     |                   |   padding within table cells   |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |        left       |  Aligns the cell's contents to |
    |                       |                     |                   |       the end of the cell      |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |       right       |  Aligns the cell's contents to |
    |                       |                     |                   |    the beginning of the cell   |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |     centerleft    |  Centers cell's contents with  |
    |                       |                     |                   | extra padding allocated to the |
    |                       |                     |                   |      beginning of the cell     |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |    centerright    |  Centers cell's contents with  |
    |                       |                     |                   | extra padding allocated to the |
    |                       |                     |                   |         end of the cell        |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |      padding_char     |         str         |                   |  Single character used to fill |
    |                       |                     |                   |   padding with. Default is a   |
    |                       |                     |                   |        blank space ` `.        |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |      newline_char     |         str         |                   | Character appended to each row |
    |                       |                     |                   | to force a newline. Default is |
    |                       |                     |                   |              `\\n`             |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |     float_rounding    |         int         |                   | Integer denoting the precision |
    |                       |                     |                   | of cells of `floats` after the |
    |                       |                     |                   |    decimal point. Default is   |
    |                       |                     |                   |             `None`.            |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |     emoji_spacing     |         str         |                   |  Strategy for rendering emojis |
    |                       |                     |                   |    in tables. Currently only   |
    |                       |                     |                   |     `mono` is supported for    |
    |                       |                     |                   |  monospaced fonts. Default is  |
    |                       |                     |                   |  `None` which disables special |
    |                       |                     |                   |       handling of emojis.      |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |       multiline       |    dict<Any,int>    |                   |     Renders the table with     |
    |                       |                     |                   | predefined widths by passing a |
    |                       |                     |                   |  `dict` with `keys` being the  |
    |                       |                     |                   |  column names (e.g. equivalent |
    |                       |                     |                   |  to those in the passed `data` |
    |                       |                     |                   |  variable) and `values` -- the |
    |                       |                     |                   |  `width` of each column as an  |
    |                       |                     |                   |  integer. Note that the width  |
    |                       |                     |                   |  of a column cannot be smaller |
    |                       |                     |                   |   than the longest contiguous  |
    |                       |                     |                   |   string present in the data.  |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |   multiline_strategy  |         str         |                   |  Strategy applied to rendering |
    |                       |                     |                   |   contents in multiple lines.  |
    |                       |                     |                   |   Possible values are `rows`,  |
    |                       |                     |                   | `header` or `rows_and_header`. |
    |                       |                     |                   |  The default value is `rows`.  |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |        rows       |  Splits only rows overfilling  |
    |                       |                     |                   | by the predefined column width |
    |                       |                     |                   | as provided in the `multiline` |
    |                       |                     |                   |            variable            |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |       header      |     Splits only the header     |
    |                       |                     |                   |  overfilling by the predefined |
    |                       |                     |                   |   column width as provided in  |
    |                       |                     |                   |    the `multiline` variable    |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |                       |                     |  rows_and_header  |     Splits rows and header     |
    |                       |                     |                   |  overfilling by the predefined |
    |                       |                     |                   |   column width as provided in  |
    |                       |                     |                   |    the `multiline` variable    |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |  multiline_delimiter  |         str         |                   | Character that will be used to |
    |                       |                     |                   |  split a cell's contents into  |
    |                       |                     |                   |   multiple rows. The default   |
    |                       |                     |                   |   value is a blank space ` `.  |
    +-----------------------+---------------------+-------------------+--------------------------------+
    |         quote         |         bool        |                   |  Wraps the generated markdown  |
    |                       |                     |                   |      table in block quotes     |
    |                       |                     |                   |     ```table```. Default is    |
    |                       |                     |                   |             `True`.            |
    +--------------------------------------------------------------------------------------------------+

    Methods
    -------
    get_header()
        gets unescaped table header
    get_body()
        gets unescaped table content
    get_markdown()
        gets complete escaped markdown table
    """

    def __init__(self, data):
        self.data: List[Dict] = data
        self.row_sep = "always"
        self.padding_width = 0
        self.padding_weight = "centerleft"
        self.padding_char = " "
        self.newline_char = "\n"
        self.float_rounding = None
        self.emoji_spacing = None
        self.multiline = None
        self.multiline_strategy = "rows"
        self.multiline_delimiter = " "
        self.quote = True
        self.validate = True
        self.__update_meta_params()

    def set_params(
        self,
        row_sep: str = "always",
        padding_width: int = 0,
        padding_weight: str = "centerleft",
        padding_char: str = " ",
        newline_char: str = "\n",
        float_rounding: Tuple[int, None] = None,
        emoji_spacing: str = None,
        multiline: Tuple[List[Dict], None] = None,
        multiline_strategy: str = "rows",
        multiline_delimiter: str = " ",
        quote: bool = True,
        validate: bool = True,
    ):
        """Setter function for markdown table rendering parameters

        Args:
            row_sep (str, optional): _description_. Defaults to "always".
            padding_width (int, optional): _description_. Defaults to 0.
            padding_weight (str, optional): _description_. Defaults to "centerleft".
            padding_char (str, optional): _description_. Defaults to " ".
            newline_char (str, optional): _description_. Defaults to "\n".
            float_rounding (Tuple[int, type, optional): _description_. Defaults to None.
            emoji_spacing (str, optional): _description_. Defaults to None.
            multiline (Tuple[List[Dict], type, optional): _description_. Defaults to None.
            multiline_strategy (str, optional): _description_. Defaults to "rows".
            multiline_delimiter (str, optional): _description_. Defaults to " ".
            quote (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        self.row_sep = row_sep
        self.padding_width = padding_width
        self.padding_weight = padding_weight
        self.padding_char = padding_char
        self.newline_char = newline_char
        self.float_rounding = float_rounding
        self.emoji_spacing = emoji_spacing
        self.multiline = multiline
        self.multiline_strategy = multiline_strategy
        self.multiline_delimiter = multiline_delimiter
        self.quote = quote
        self.validate = validate
        if validate:
            self.__validate_parameters()
        self.__update_meta_params()
        return self

    def __update_meta_params(self):
        if self.multiline:
            self.var_padding = self.multiline
            # add user-defined padding to the provided multiline column width dict
            for key, value in self.var_padding.items():
                self.var_padding[key] = value + self.padding_width
        else:
            self.var_padding = self.__get_padding()
        self.var_row_sep = self.__get_row_sep_str()
        self.var_row_sep_last = self.__get_row_sep_last()

    def __validate_parameters(self):
        row_sep_values = ["always", "topbottom", "markdown", None]
        padding_weight_values = ["left", "right", "centerleft", "centerright"]
        emoji_spacing_values = ["mono", None]
        multiline_strategy_values = ["rows", "header", "rows_and_header"]
        if self.row_sep not in row_sep_values:
            raise ValueError(
                f"row_sep value of '{self.row_sep}' is not valid. \
                    Possible values are {*row_sep_values,}."
            )
        if not isinstance(self.padding_width, int):
            raise ValueError(
                f"padding_width value of '{self.padding_width}' is not valid. \
                    Please use an integer."
            )
        if self.padding_weight not in padding_weight_values:
            raise ValueError(
                f"padding_weight value of '{self.row_sep}' is not valid. \
                    Possible values are {*padding_weight_values,}."
            )
        if not isinstance(self.padding_char, str) or len(str(self.padding_char)) != 1:
            raise ValueError(
                f"padding_char value of '{self.padding_char}' is not valid. \
                    Please use a single character string."
            )
        # Do not check for the validity of a newline character
        # self.newline_char = newline_char
        if not isinstance(self.float_rounding, (type(None), int)):
            raise ValueError(
                f"float_rounding value of '{self.float_rounding}' is not valid. \
                    Please use an integer or leave as None."
            )
        if self.emoji_spacing not in emoji_spacing_values:
            raise ValueError(
                f"emoji_spacing value of '{self.emoji_spacing}' is not valid. \
                    Possible values are {*emoji_spacing_values,}."
            )
        if not isinstance(self.multiline, (type(None), dict)):
            raise ValueError(
                f"multiline value of '{self.multiline}' is not valid. \
                    Please use an dict or leave as None."
            )
        if self.multiline_strategy not in multiline_strategy_values:
            raise ValueError(
                f"multiline_strategy value of '{self.multiline_strategy}' is not valid. \
                    Possible values are {*multiline_strategy_values,}."
            )
        if not isinstance(self.multiline_delimiter, str) or len(str(self.multiline_delimiter)) != 1:
            raise ValueError(
                f"multiline_delimiter value of '{self.multiline_delimiter}' is not valid. \
                    Please use a single character string."
            )
        if not isinstance(self.quote, bool):
            raise ValueError(
                f"quote value of '{self.quote}' is not valid. \
                    Please use a boolean."
            )

    def __validate_data(self):
        if len(self.data) < 1:
            raise ValueError("Data variable contains no elements.")
        keys = self.data[0].keys()
        for item in self.data:
            for key in keys:
                if key not in item:
                    raise ValueError("Dictionary keys are not uniform across data variable.")
        if self.multiline:
            for row in self.data:
                for key, item in row.items():
                    multiline_data = row[key].split(self.multiline_delimiter)
                    multiline_max_width = max(multiline_data, key=len)
                    if (self.var_padding[key]) < (len(multiline_max_width) + self.padding_width):
                        raise ValueError(
                            f"Contiguous string exists longer than the \
                                allocated column width for column '{key}' \
                                    and padding_width '{self.padding_width}'."
                        )

    def __get_padding(self):
        """Calculate table-wide padding. Internal method, which should never be called."""
        padding = {}
        for item in self.data[0].keys():
            padding[item] = len(item)
        for item in self.data:
            for key in item.keys():
                if self.float_rounding and isinstance(item[key], float):
                    item[key] = round(item[key], self.float_rounding)
                # prepend float pre-processing
                if (padding[key] - self.padding_width) < len(str(item[key])):
                    padding[key] = len(str(item[key])) + self.padding_width
                # prepend emoji pre-processing
                emoji = []
                if self.emoji_spacing == "mono":
                    emoji = count_emojis(item[key])
                # adapt padding with all information
                if padding[key] - self.padding_width - len(emoji) < len(str(item[key])):
                    padding[key] = len(str(item[key])) + self.padding_width + len(emoji)
        return padding

    def __get_row_sep_str(self):
        row_sep_str = ""
        for value in self.var_padding.values():
            row_sep_str += "+" + "-" * value
        row_sep_str += "+"
        return row_sep_str

    def __get_row_sep_last(self):
        row_sep_str_last = "+"
        for value in self.var_padding.values():
            row_sep_str_last += "-" * (value + 1)
        row_sep_str_last = row_sep_str_last[:-1] + "+"
        return row_sep_str_last

    def __get_margin(self, margin):
        if self.padding_weight == "left":
            right = 0
        elif self.padding_weight == "right":
            right = margin
        elif self.padding_weight == "centerleft":
            right = math.floor(margin / 2)
        elif self.padding_weight == "centerright":
            right = math.ceil(margin / 2)
        else:
            right = math.floor(margin / 2)
        return right

    def __get_row(self, item):
        # checking if multiline variable for rows is set
        if self.multiline and self.multiline_strategy in ["rows", "rows_and_header"]:
            # local check if row needs to be split in multiple lines
            multiline = False
            for key in self.data[0].keys():
                if len(item[key]) > self.var_padding[key]:
                    multiline = True
            if multiline:
                return self.__get_multiline_row(item)
            return self.__get_normal_row(item)
        # if multiline is not set it's not multiline and return regular row
        return self.__get_normal_row(item)

    def __get_normal_row(self, item):
        row = ""
        for key in self.data[0].keys():
            # prepend emoji pre-processing for cell values
            emoji = []
            if self.emoji_spacing == "mono":
                emoji = count_emojis(item[key])
            # extract column padding to local variable so that if emojis are present
            # the cell can be rendered with the extra spacing needed
            local_padding = self.var_padding[key] - len(emoji)
            margin = local_padding - len(str(item[key]))
            right = self.__get_margin(margin)
            row += "|" + str(item[key]).rjust(local_padding - right, self.padding_char).ljust(
                local_padding, self.padding_char
            )
        row += "|"
        return row

    def __get_multiline_row(self, item):
        multiline_items = {}
        # process multiline rows column by column
        for key in self.data[0].keys():
            # split cell's contents by delimiter
            delimiter_split_cell = item[key].split(self.multiline_delimiter)
            fully_split_cell = []
            # iterate over each element in the split
            for element in delimiter_split_cell:
                emojis = count_emojis(element)
                # if no emojis are found just append the element
                if len(emojis) == 0:
                    fully_split_cell.append(element)
                # if emojis are present, split by emoji into a list and concat
                else:
                    emoji_indices = [emoji["index"] for emoji in emojis if "index" in emoji]
                    emoji_split_element = split_list_by_indices(element, emoji_indices)
                    fully_split_cell = fully_split_cell + emoji_split_element

            multiline_row = []
            single_row = []
            item_prev_length = 0
            spacing_between_items = 0
            while len(fully_split_cell) > 0:
                # check item length and adjust for presence of emoji
                # only check the first element since we are using a stack
                item_length = len(fully_split_cell[0]) + len(count_emojis(fully_split_cell[0]))

                if item_length + item_prev_length + spacing_between_items + self.padding_width <= self.var_padding[key]:
                    # count just the items
                    item_prev_length += item_length
                    # add item to the current row
                    single_row.append(fully_split_cell.pop(0))
                    # calculate the required spacing
                    spacing_between_items = len(single_row)
                else:
                    multiline_row.append(" ".join(single_row))
                    single_row = []
                    # added element, clear buffer and spacing variable
                    item_prev_length = 0
                    spacing_between_items = 0
            multiline_row.append(" ".join(single_row))
            multiline_items[key] = multiline_row

        # get the max row count in the multiline item
        multiline_rows_max = max(map(len, multiline_items.values()))

        # fill in blank values for multiline rows below this maximum
        for key, value in multiline_items.items():
            if len(value) < multiline_rows_max:
                for _ in range(len(value), multiline_rows_max):
                    value.append(self.padding_char * self.var_padding[key])

        # since we are rendering a single row over multiple columns
        # access the multiline_rows dictionary by index rather than key
        rows = ""
        for i in range(0, multiline_rows_max):
            row_dict = {}
            for key in self.data[0].keys():
                row_dict[key] = multiline_items[key][i]
            rows += self.__get_normal_row(row_dict)
            if i < multiline_rows_max - 1:
                rows += self.newline_char
        return rows

    def get_header(self):
        """Get the header of the markdown table"""
        header = ""
        if self.row_sep in ["topbottom", "always"]:
            header += self.newline_char + self.var_row_sep_last + self.newline_char

        # if header is set to be multirow
        if self.multiline and self.multiline_strategy in ["header", "rows_and_header"]:
            # invert keys with values, so that we can reuse the multiline row function
            inv_data = {k: k for k, v in self.data[0].items()}
            header += self.__get_multiline_row(inv_data)
            header += self.newline_char
        # else header is not rendered as multiple rows
        else:
            for key in self.data[0].keys():
                margin = self.var_padding[key] - len(key)
                right = self.__get_margin(margin)
                header += "|" + key.rjust(self.var_padding[key] - right, self.padding_char).ljust(
                    self.var_padding[key], self.padding_char
                )
            header += "|" + self.newline_char

        if self.row_sep == "always":
            header += self.var_row_sep + self.newline_char
        if self.row_sep == "markdown":
            header += self.var_row_sep.replace("+", "|") + self.newline_char
        return header

    def get_body(self):
        """Get the body of the markdown table"""
        rows = ""
        for i, item in enumerate(self.data):
            rows += self.__get_row(item)
            if i < len(self.data) - 1:
                rows += self.newline_char
            if self.row_sep == "always" and i < len(self.data) - 1:
                rows += self.var_row_sep + self.newline_char
            if self.row_sep in ["topbottom", "always"] and i == len(self.data) - 1:
                rows += self.newline_char + self.var_row_sep_last
        return rows

    def get_markdown(self):
        """Get the complete markdown table"""
        self.__validate_data()
        self.__update_meta_params()
        data = self.get_header() + self.get_body()
        if self.quote:
            return "```" + data + "```"
        return data
