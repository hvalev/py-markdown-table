# -*- coding: utf-8 -*-
"""Class used to generate formatted markdown tables. See class description"""
import math
from typing import Optional, List, Dict, Union
from py_markdown_table.utils import count_emojis, split_list_by_indices


class markdown_table:  # noqa: N801
    """
    Class used to generate padded tables in a markdown code block

    Methods
    -------
    get_markdown()
        gets complete escaped markdown table
    get_header()
        gets unescaped table header
    get_body()
        gets unescaped table content
    """

    def __init__(
        self, 
        data: Union[List[Dict], Dict],
        skip_data_validation: bool = False,
    ):
        """
        Initialize markdown_table with support for various rendering parameters.

        Args:
        `data` (List[Dict]): The data to be rendered in the markdown table. \n
        `skip_data_validation` (bool, optional): skip the data validation step before rending a table. Useful when renderers change the length of a string (i.e. markdown urls). \n
            Default is `False` \n

        """
        if not isinstance(data, list) or not all(isinstance(elem, dict) for elem in data):
            raise ValueError("data is not of type list or elements are not of type dict")
        if len(data) == 0:
            raise ValueError("Data variable contains no elements.")
        self.data = data

        # set defaults
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

        if not skip_data_validation:
            self.__validate_data(data)

        self.__validate_parameters()
        self.__update_meta_params()
        
    def set_params(
        self,
        row_sep: str = "always",
        padding_width: int = 0,
        padding_weight: str = "centerleft",
        padding_char: str = " ",
        newline_char: str = "\n",
        float_rounding: Optional[int] = None,
        emoji_spacing: Optional[str] = None,
        multiline: Optional[Dict] = None,
        multiline_strategy: str = "rows",
        multiline_delimiter: str = " ",
        quote: bool = True,
    ):
        """
        Setter function for markdown table rendering parameters.

        Args:
        `row_sep` (str, optional): Row separation strategy using `----` as pattern. Possible values are:
            `always`: Separate each row.
            `topbottom`: Separate the top (header) and bottom (last row) of the table.
            `markdown`: Separate only the header from the body.
            `None`: No row separators will be inserted. Defaults to "always". \n
        `padding_width` (int, optional): Width of padding to allocate to all table cells. Defaults to `0`. \n
        `padding_weight` (str, optional): Strategy for allocating padding within table cells. Possible values are:
            `left`: Aligns the cell's contents to the end of the cell.
            `right`: Aligns the cell's contents to the beginning of the cell.
            `centerleft`: Centers cell's contents with extra padding allocated to the beginning of the cell.
            `centerright`: Centers cell's contents with extra padding allocated to the end of the cell.
            Defaults to `centerleft`. \n
        `padding_char` (str, optional): Single character used to fill padding. Default is a blank space ` `. \n
        `newline_char` (str, optional): Character appended to each row to force a newline. Default is `\\n`. \n
        `float_rounding` (Optional[int], optional): Integer denoting the precision of cells with `float` values after the decimal point. 
            Default is `None`. \n
        `emoji_spacing` (Optional[str], optional): Strategy for rendering emojis in tables. 
            `mono` will emojis as single characters, suitable for monospaced fonts.
            `None` will not detect and process emojis. 
            Default is `None`. \n
        `multiline` (Optional[Dict[str, int]], optional): Renders the table with predefined widths by passing a dictionary with column names as keys and their respective widths as values. Note that the width of a column cannot be smaller than the longest contiguous string present in the data.
            Default is `None`. \n
        `multiline_strategy` (str, optional): Strategy applied to rendering contents in multiple lines. Possible values are:
            `rows`: Splits only rows overfilling the predefined column width.
            `header`: Splits only the header overfilling the predefined column width.
            `rows_and_header`: Splits rows and header overfilling the predefined column width.
            Default is `rows`. \n
        `multiline_delimiter` (str, optional): Character that will be used to split a cell's contents into multiple rows.
            Default is a blank space ` `. \n
        `quote` (bool, optional): Wraps the generated markdown table in block quotes ` ```table``` `. 
            Default is `True`.

        Returns:
            self: Returns the instance with updated parameters.
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
        
        self.__validate_parameters()
        self.__update_meta_params()
        return self

    def __update_meta_params(self):
        """Update and store internal meta-parameters"""
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
        valid_values = {
            "row_sep": ["always", "topbottom", "markdown", None],
            "padding_weight": ["left", "right", "centerleft", "centerright"],
            "emoji_spacing": ["mono", None],
            "multiline_strategy": ["rows", "header", "rows_and_header"]
        }

        for attr, values in valid_values.items():
            if getattr(self, attr) not in values:
                raise ValueError(f"{attr} value of '{getattr(self, attr)}' is not valid. Possible values are {values}.")

        if not isinstance(self.padding_width, int):
            raise ValueError(f"padding_width value of '{self.padding_width}' is not valid. Please use an integer.")

        if not isinstance(self.padding_char, str) or len(self.padding_char) != 1:
            raise ValueError(f"padding_char value of '{self.padding_char}' is not valid. Please use a single character string.")

        if not isinstance(self.float_rounding, (type(None), int)):
            raise ValueError(f"float_rounding value of '{self.float_rounding}' is not valid. Please use an integer or leave as None.")

        if not isinstance(self.multiline, (type(None), dict)):
            raise ValueError(f"multiline value of '{self.multiline}' is not valid. Please use a dict or leave as None.")

        if not isinstance(self.multiline_delimiter, str) or len(self.multiline_delimiter) != 1:
            raise ValueError(f"multiline_delimiter value of '{self.multiline_delimiter}' is not valid. Please use a single character string.")

        if not isinstance(self.quote, bool):
            raise ValueError(f"quote value of '{self.quote}' is not valid. Please use a boolean.")


    def __validate_data(self, data):
        # Check if all dictionaries in self.data have uniform keys
        keys = set(data[0].keys())  # Use set for fast lookup
        for item in data:
            if not isinstance(item, dict):
                raise TypeError("Each element in data must be a dictionary.")
            if set(item.keys()) != keys:
                raise ValueError("Dictionary keys are not uniform across data variable.")

        if self.multiline:
            for row in data:
                for key in row.keys():
                    if key in self.var_padding:
                        multiline_data = row[key].split(self.multiline_delimiter)
                        multiline_max_width = max(multiline_data, key=len)
                        if len(multiline_max_width) + self.padding_width > self.var_padding[key]:
                            raise ValueError(
                                f"Contiguous string exists longer than the allocated column width "
                                f"for column '{key}' and padding_width '{self.padding_width}'."
                            )
                    else:
                        raise KeyError(f"Key '{key}' not found in var_padding.")

    def __get_padding(self):
        """Calculate table-wide padding."""
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
            # preprend emoji pre-processing for cell values
            emoji = []
            if self.emoji_spacing == "mono":
                emoji = count_emojis(item[key])
            # extract column padding to local variable so that if emojis are present
            # the cell can be rendered with the extra spacing needed
            local_padding = self.var_padding[key] - len(emoji)
            margin = local_padding - len(str(item[key]))
            right = self.__get_margin(margin)
            row += "|" + str(item[key]).rjust(
                local_padding - right, self.padding_char
            ).ljust(local_padding, self.padding_char)
        row += "|"
        return row

    def __get_multiline_row(self, item):
        multiline_items = {}

        # Helper function to process each element and split by emojis if present
        def split_and_process_element(element):
            emojis = count_emojis(element)
            if not emojis:
                return [element]
            emoji_indices = [emoji["index"] for emoji in emojis if "index" in emoji]
            return split_list_by_indices(element, emoji_indices)

        # Process each column in the row
        for key in self.data[0].keys():
            fully_split_cell = []
            # Split cell content by the delimiter and process each part
            for element in item[key].split(self.multiline_delimiter):
                fully_split_cell.extend(split_and_process_element(element))

            multiline_row, single_row = [], []
            item_prev_length, spacing_between_items = 0, 0

            # Create multiline rows from the split elements
            while fully_split_cell:
                current_element = fully_split_cell[0]
                item_length = len(current_element) + len(count_emojis(current_element))

                # Check if the current element fits in the row
                if item_length + item_prev_length + spacing_between_items + self.padding_width <= self.var_padding[key]:
                    item_prev_length += item_length
                    single_row.append(fully_split_cell.pop(0))
                    spacing_between_items = len(single_row)
                else:
                    # Start a new line if the current element doesn't fit
                    multiline_row.append(" ".join(single_row))
                    single_row, item_prev_length, spacing_between_items = [], 0, 0

            # Add the remaining elements in single_row to multiline_row
            multiline_row.append(" ".join(single_row))
            multiline_items[key] = multiline_row

        # Find the maximum number of rows in any column
        multiline_rows_max = max(map(len, multiline_items.values()))

        # Pad columns with fewer rows to ensure all columns have the same number of rows
        for key, value in multiline_items.items():
            value.extend([self.padding_char * self.var_padding[key]] * (multiline_rows_max - len(value)))

        rows = ""
        # Create the final output by combining rows from each column
        for i in range(multiline_rows_max):
            row_dict = {key: multiline_items[key][i] for key in self.data[0].keys()}
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
            inv_data = {k: k for k, _ in self.data[0].items()}
            header += self.__get_multiline_row(inv_data)
            header += self.newline_char
        # else header is not rendered as multiple rows
        else:
            for key in self.data[0].keys():
                margin = self.var_padding[key] - len(key)
                right = self.__get_margin(margin)
                header += "|" + key.rjust(
                    self.var_padding[key] - right, self.padding_char
                ).ljust(self.var_padding[key], self.padding_char)
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
        self.__update_meta_params()
        data = self.get_header() + self.get_body()
        if self.quote:
            return "```" + data + "```"
        return data