# -*- coding: utf-8 -*-
"""Class used to generate formatted markdown tables. See class description"""
import math
from typing import Any
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

    # Declared here rather than inferred from the constructor, because
    # set_params reassigns all of them later on.
    row_sep: str | None
    padding_width: dict[str, int]
    padding_weight: dict[str, str]
    padding_char: str
    newline_char: str
    float_rounding: int | None
    emoji_spacing: str | None
    multiline: dict[str, int] | None
    multiline_strategy: str
    multiline_delimiter: str
    quote: bool
    compact: bool
    skip_data_validation: bool
    # derived by __update_meta_params, needed by every render entry point
    var_padding: dict[str, int]
    var_row_sep: str
    var_row_sep_last: str
    # every value rendered to a string, measured and wrapped from this copy
    _cells: list[dict[str, str]]

    def __init__(
        self,
        data: list[dict[str, Any]],
        skip_data_validation: bool = False,
    ) -> None:
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
        # own copy: rendering must never write back into the caller's rows
        self.data = [dict(row) for row in data]

        # set defaults
        self.row_sep = "always"
        self.padding_width = dict.fromkeys(self.data[0].keys(), 0)
        self.padding_weight = dict.fromkeys(self.data[0].keys(), "centerleft")
        self.padding_char = " "
        self.newline_char = "\n"
        self.float_rounding = None
        self.emoji_spacing = None
        self.multiline = None
        self.multiline_strategy = "rows"
        self.multiline_delimiter = " "
        self.quote = True
        self.compact = False
        self.skip_data_validation = skip_data_validation

        self.__validate_parameters()
        
        if not self.skip_data_validation:
            self.__validate_data(data)

        self.__validate_column_keys()
        self.__prepare_cells()
        self.__update_meta_params()

        # we need to first update the meta_params for cell width, padding etc
        # prior to checking whether the data will fit for multiline rendering
        if self.multiline:
            self.__validate_multiline()
        

    def set_params(
        self,
        row_sep: str | None = "always",
        padding_width: int | dict[str, int] = 0,
        padding_weight: str | dict[str, str] = "centerleft",
        padding_char: str = " ",
        newline_char: str = "\n",
        float_rounding: int | None = None,
        emoji_spacing: str | None = None,
        multiline: dict[str, int] | None = None,
        multiline_strategy: str = "rows",
        multiline_delimiter: str = " ",
        quote: bool = True,
        compact: bool = False,
    ) -> "markdown_table":
        """
        Setter function for markdown table rendering parameters.

        Args:
        `row_sep` (str, optional): Row separation strategy using `----` as pattern. Possible values are:
            `always`: Separate each row.
            `topbottom`: Separate the top (header) and bottom (last row) of the table.
            `markdown`: Separate only the header from the body.
            `None`: No row separators will be inserted. Defaults to "always". \n
        `padding_width` (int | dict[str, int], optional): Extra columns a column gets on top of its widest cell. This is one pool of slack per column, not one per side - `padding_weight` decides how the pool is split between the left and the right. Defaults to `0`. Padding can also be assigned per column by passing key-value pairs whose keys are exactly the columns of the input data.\n
        `padding_weight` (str | dict[str, str], optional): How the `padding_width` of a column is distributed between its left and its right side. Can be assigned globally for the whole table as a string or per-column by passing key-value pairs whose keys are exactly the columns of the input data. Possible values are:
            `left`: Aligns the cell's contents to the end of the cell.
            `right`: Aligns the cell's contents to the beginning of the cell.
            `centerleft`: Centers cell's contents with extra padding allocated to the beginning of the cell.
            `centerright`: Centers cell's contents with extra padding allocated to the end of the cell.
            Defaults to `centerleft`. \n
        `padding_char` (str, optional): Single character used to fill padding. Default is a blank space ` `. \n
        `newline_char` (str, optional): Character appended to each row to force a newline. Default is `\\n`. \n
        `float_rounding` (int, optional): Number of digits to keep after the decimal point of `float` cells, rounding them to that precision. Must be 0 or greater; `None` leaves floats untouched. 
            Default is `None`. \n
        `emoji_spacing` (str, optional): Strategy for rendering characters that a monospace font draws two columns wide.
            `mono` budgets two columns for each of them, so a column of emoji or CJK ends up the width it occupies on screen. Which characters those are comes from `unicodedata.east_asian_width`.
            `None` treats every character as one column wide. 
            Default is `None`. \n
        `multiline` (dict[str, int], optional): Wrap columns to the given widths, as a dictionary with a width per column. The width is the space left for content, so `padding_width` is added on top of it rather than taken from it. Values must be provided for every column.
            A word that does not fit the width is refused rather than allowed to overrun the column, and a run of wide characters may be broken between characters.
            Line breaks inside a value are rendered as extra lines only in this mode; without it they are refused, because they would split a row across two output lines.
            Default is `None`. \n
        `multiline_strategy` (str, optional): Strategy applied to rendering contents in multiple lines. Possible values are:
            `rows`: Splits only rows overfilling the predefined column width.
            `header`: Splits only the header overfilling the predefined column width.
            `rows_and_header`: Splits rows and header overfilling the predefined column width.
            Default is `rows`. \n
        `multiline_delimiter` (str, optional): Character a cell's contents are split on to find places to wrap, and put back between the parts that end up on one line.
            Default is a blank space ` `. \n
        `quote` (bool, optional): Wraps the generated markdown table in block quotes ` ```table``` `. 
            Default is `True`. 

        `compact` (bool, optional): Emit the smallest table that is still valid markdown: cells are not padded and the header separator is a single `-` per column. Only meaningful when the renderer draws the table, so it requires `row_sep` `markdown`. Widths given to `multiline` are still honoured, they just no longer add padding. Default is `False`.

        Returns:
            self: Returns the instance with updated parameters.
        """
        self.row_sep = row_sep
        # one value for the whole table is spread over every column, so the
        # attribute only ever holds the per-column mapping
        self.padding_width = (
            dict.fromkeys(self.data[0].keys(), padding_width)
            if isinstance(padding_width, int)
            else padding_width
        )
        self.padding_weight = (
            dict.fromkeys(self.data[0].keys(), padding_weight)
            if isinstance(padding_weight, str)
            else padding_weight
        )
        self.padding_char = padding_char
        self.newline_char = newline_char
        self.float_rounding = float_rounding
        self.emoji_spacing = emoji_spacing
        self.multiline = multiline
        self.multiline_strategy = multiline_strategy
        self.multiline_delimiter = multiline_delimiter
        self.quote = quote
        self.compact = compact

        
        self.__validate_parameters()
        
        if not self.skip_data_validation:
            self.__validate_data(self.data)

        self.__validate_column_keys()
        self.__prepare_cells()

        self.__update_meta_params()
        
        if self.multiline:
            self.__validate_multiline()

        return self

    def __update_meta_params(self) -> None:
        """Update and store internal meta-parameters"""
        if self.multiline:
            # copy, and add padding exactly once: assigning self.multiline here
            # made every render widen the columns again and corrupted the
            # dictionary the caller passed in
            self.var_padding = {key: value + self.padding_width[key] for key, value in self.multiline.items()}
        else:
            self.var_padding = self.__get_padding()
        self.var_row_sep = self.__get_row_sep_str()
        # self.var_row_sep_last = self.__get_row_sep_last()
        self.var_row_sep_last = self.__get_row_sep_str()

    def __validate_parameters(self) -> None:  # noqa: C901
        valid_values: dict[str, list[Any]] = {
            "row_sep": ["always", "topbottom", "markdown", None],
            "emoji_spacing": ["mono", None],
            "multiline_strategy": ["rows", "header", "rows_and_header"]
        }

        valid_dict_values = {
            "padding_weight": ["left", "right", "centerleft", "centerright"],
        }

        # Validate fixed value attributes
        for attr, values in valid_values.items():
            if getattr(self, attr) not in values:
                raise ValueError(f"{attr} value of '{getattr(self, attr)}' is not valid. Possible values are {values}.")

        # Validate padding_weight
        if isinstance(self.padding_weight, dict):
            for column, weight in self.padding_weight.items():
                if weight not in valid_dict_values["padding_weight"]:
                    raise ValueError(f"padding_weight[{column}] value of '{weight}' is not valid. Possible values are {valid_dict_values['padding_weight']}.")
        else:
            raise ValueError(f"padding_weight value of '{self.padding_weight}' is not valid.")

        # Validate padding_width
        if isinstance(self.padding_width, dict):
            for column, width in self.padding_width.items():
                if not isinstance(width, int) or not (0 <= width < 100000):
                    raise ValueError(f"padding_width[{column}] value of '{width}' is not valid. Possible range is 0 <= width < 100000.")
        else:
            raise ValueError(f"padding_width value of '{self.padding_width}' is not valid.")

        # Validate padding_char
        if not isinstance(self.padding_char, str) or len(self.padding_char) != 1:
            raise ValueError(f"padding_char value of '{self.padding_char}' is not valid. Please use a single character string.")

        # Validate float_rounding
        if not isinstance(self.float_rounding, (type(None), int)) or (
            isinstance(self.float_rounding, int) and self.float_rounding < 0
        ):
            raise ValueError(
                f"float_rounding value of '{self.float_rounding}' is not valid. Please use an integer >= 0 or leave as None."
            )

        # Validate multiline
        if not isinstance(self.multiline, (type(None), dict)):
            raise ValueError(f"multiline value of '{self.multiline}' is not valid. Please use a dict or leave as None.")

        # Validate multiline_delimiter
        if not isinstance(self.multiline_delimiter, str) or len(self.multiline_delimiter) != 1:
            raise ValueError(f"multiline_delimiter value of '{self.multiline_delimiter}' is not valid. Please use a single character string.")

        # Validate quote
        if not isinstance(self.quote, bool):
            raise ValueError(f"quote value of '{self.quote}' is not valid. Please use a boolean.")

        # Validate compact
        if not isinstance(self.compact, bool):
            raise ValueError(f"compact value of '{self.compact}' is not valid. Please use a boolean.")
        if self.compact and self.row_sep != "markdown":
            raise ValueError(
                "compact output requires row_sep 'markdown'. Without the separators a renderer "
                "draws for you, an unpadded table is unreadable where the characters themselves "
                "form the borders."
            )

    def __validate_column_keys(self) -> None:
        """Per-column option dicts must cover exactly the table columns."""
        columns = set(self.data[0].keys())
        for name in ("padding_width", "padding_weight", "multiline"):
            value = getattr(self, name)
            if not isinstance(value, dict):
                continue
            unknown = sorted(set(value) - columns, key=str)
            missing = sorted(columns - set(value), key=str)
            if unknown:
                raise ValueError(f"{name} contains key(s) that are not columns of the table: {unknown}. The columns are {sorted(columns, key=str)}.")
            if missing:
                raise ValueError(f"{name} has no value for column(s): {missing}. The columns are {sorted(columns, key=str)}.")

    def __prepare_cells(self) -> None:
        """Render every value to a string once, before any measuring.

        Downstream code splits cells, scans them for emojis and takes their
        length, so normalising here makes the plain, multiline and emoji paths
        accept the same value types. Rounding happens here rather than while
        measuring so that no caller data is ever written to.
        """
        self._cells = []
        for row in self.data:
            cell = {}
            for key, value in row.items():
                if self.float_rounding and isinstance(value, float):
                    value = round(value, self.float_rounding)
                # a line break is a line break whichever platform produced it;
                # left alone, a bare carriage return is one column wide here
                # and something else entirely in the renderer
                text = str(value).replace("\r\n", "\n").replace("\r", "\n")
                cell[key] = text
            self._cells.append(cell)

    def __reject_line_breaks(self) -> None:
        """Without column widths there is no way to render a line break.

        The row simply continues on the next output line, which leaves the
        table ragged and, in markdown mode, is no longer a table at all.
        """
        for i, row in enumerate(self._cells):
            for key, value in row.items():
                if "\n" in value:
                    raise ValueError(
                        f"The value in the element [{i}] under column '{key}' contains a line "
                        f"break. Either give that column a `multiline` width so it can be wrapped, "
                        f"or replace the line break in the data."
                    )

    def __validate_data(self, data: list[dict[str, Any]]) -> None:
        # Check if all dictionaries in self.data have uniform keys
        keys = set(data[0].keys())
        for item in data:
            if not isinstance(item, dict):
                raise TypeError("Each element in data must be a dictionary.")
            if set(item.keys()) != keys:
                raise ValueError("Dictionary keys are not uniform across data variable.")

    def __validate_multiline(self) -> None:
        for i, row in enumerate(self._cells):
            for key in row.keys():
                if key not in self.var_padding:
                    raise KeyError(f"Key '{key}' not found in var_padding.")
                # the header goes through the same wrapping code only when the
                # strategy renders it, so otherwise it has to fit whole
                if self.multiline_strategy in ["header", "rows_and_header"]:
                    values = [key, row[key]]
                else:
                    values = [row[key]]
                    if self.__display_width(key) > self.var_padding[key]:
                        raise ValueError(
                            f"The column name '{key}' is wider than the column width "
                            f"allocated for it and cannot be wrapped by the "
                            f"multiline_strategy '{self.multiline_strategy}'."
                        )
                for value in values:
                    for line in value.split("\n"):
                        for piece, _ in self.__line_pieces(line):
                            if self.__display_width(piece) > self.__content_width(key):
                                raise ValueError(
                                    f"There is a contiguous string:\n"
                                    f"'{piece}'\n"
                                    f"in the element [{i}] "
                                    f"which is longer than the allocated column width "
                                    f"for column '{key}' and padding_width '{self.padding_width[key]}'."
                                )

    def __display_width(self, value: str) -> int:
        """Columns a value occupies when drawn.

        One column per character, except in mono emoji mode, where each emoji
        is drawn roughly twice as wide as the single code point it is made of.
        """
        if self.emoji_spacing == "mono":
            return len(value) + len(count_emojis(value))
        return len(value)

    def __content_width(self, key: str) -> int:
        """Room left for content once the column padding is taken off."""
        return self.var_padding[key] - self.padding_width[key]

    def __line_pieces(self, line: str) -> list[tuple[str, str]]:
        """Pieces a rendered line may be cut between, and what joins each one.

        Words come from `multiline_delimiter`. An emoji is a break opportunity
        on both sides, which is what lets a run of emoji wrap instead of
        overflowing the column. Pieces cut out of the same word join with
        nothing, so re-assembling a line reproduces the value character for
        character - the joining used to use the delimiter here, which turned
        `a\U0001f600b` into `a \U0001f600 b`.
        """
        pieces = []
        for position, word in enumerate(line.split(self.multiline_delimiter)):
            parts = [word]
            if self.emoji_spacing == "mono":
                indices = [emoji["index"] for emoji in count_emojis(word)]
                if indices:
                    parts = split_list_by_indices(word, indices)
            for part_index, part in enumerate(parts):
                gap = self.multiline_delimiter if not part_index and position else ""
                pieces.append((part, gap))
        return pieces

    @staticmethod
    def __join_pieces(pieces: list[tuple[str, str]]) -> str:
        """Put pieces back into one line; the first one keeps no separator."""
        line = ""
        for position, (text, gap) in enumerate(pieces):
            line += text if position == 0 else gap + text
        return line

    def __get_padding(self) -> dict[str, int]:
        """Calculate table-wide padding from the prepared cells."""
        padding = {key: len(key) for key in self.data[0].keys()}
        for row in self._cells:
            for key, value in row.items():
                width = self.__display_width(value)
                if padding[key] < width + self.padding_width[key]:
                    padding[key] = width + self.padding_width[key]
        return padding

    def __get_row_sep_str(self) -> str:
        if self.compact:
            return "|" + "|".join("-" for _ in self.var_padding) + "|"
        row_sep_str = ""
        for value in self.var_padding.values():
            row_sep_str += "+" + "-" * value
        row_sep_str += "+"
        return row_sep_str

    def __get_margin(self, margin: int, key: str) -> int:
        # get column-specific alignment based on the column key (header)
        if self.padding_weight[key] == "left":
            right = 0
        elif self.padding_weight[key] == "right":
            right = margin
        elif self.padding_weight[key] == "centerleft":
            right = math.floor(margin / 2)
        elif self.padding_weight[key] == "centerright":
            right = math.ceil(margin / 2)
        else:
            right = math.floor(margin / 2)
        return right

    def __get_row(self, item: dict[str, str]) -> str:
        # checking if multiline variable for rows is set
        if self.multiline and self.multiline_strategy in ["rows", "rows_and_header"]:
            # local check if row needs to be split in multiple lines
            multiline = False
            for key in self.data[0].keys():
                if self.__display_width(item[key]) > self.__content_width(key):
                    multiline = True
                if "\n" in item[key]:
                    multiline = True

            if multiline:
                return self.__get_multiline_row(item)
            return self.__get_normal_row(item)
        # if multiline is not set it's not multiline and return regular row
        return self.__get_normal_row(item)

    def __get_normal_row(self, item: dict[str, str]) -> str:
        if self.compact:
            return "|" + "|".join(str(item[key]) for key in self.data[0].keys()) + "|"
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
            right = self.__get_margin(margin, key)
            row += "|" + str(item[key]).rjust(
                local_padding - right, self.padding_char
            ).ljust(local_padding, self.padding_char)
        row += "|"
        return row

    def __get_multiline_row(self, item: dict[str, str]) -> str:  # noqa: C901
        multiline_items = {}

        # Process each column in the row
        for key in self.data[0].keys():
            multiline_row = []
            # First we split by embedded line breaks in order to correctly
            # render lists and othe markdown elements which depend on newline offset
            for line in item[key].split("\n"):
                # measure the line that would actually be printed, in the
                # unit the terminal draws it, against the room left for content
                remaining = self.__line_pieces(line)
                single_row: list[tuple[str, str]] = []
                while remaining:
                    candidate = single_row + [remaining[0]]
                    # a piece too wide for a line of its own still gets one,
                    # rather than being reconsidered forever
                    if len(candidate) == 1 or self.__display_width(
                        self.__join_pieces(candidate)
                    ) <= self.__content_width(key):
                        single_row = candidate
                        remaining.pop(0)
                    else:
                        multiline_row.append(self.__join_pieces(single_row))
                        single_row = []
                if single_row:
                    multiline_row.append(self.__join_pieces(single_row))
            multiline_items[key] = multiline_row

        # Find the maximum number of rows in any column
        multiline_rows_max = max(map(len, multiline_items.values()))

        # Pad columns with fewer rows to ensure all columns have the same number of rows
        for key, value in multiline_items.items():
            # in compact mode an empty cell is an empty string, not a run of
            # padding characters
            filler = "" if self.compact else self.padding_char * self.var_padding[key]
            value.extend([filler] * (multiline_rows_max - len(value)))

        rows = ""
        # Create the final output by combining rows from each column
        for i in range(multiline_rows_max):
            row_dict = {key: multiline_items[key][i] for key in self.data[0].keys()}
            rows += self.__get_normal_row(row_dict)
            if i < multiline_rows_max - 1:
                rows += self.newline_char
        return rows


    def get_header(self) -> str:
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
        elif self.compact:
            # the header is just another row of values, without the padding
            header += self.__get_normal_row({key: key for key in self.data[0].keys()}) + self.newline_char
        else:
            for key in self.data[0].keys():
                margin = self.var_padding[key] - len(key)
                right = self.__get_margin(margin, key)
                header += "|" + key.rjust(
                    self.var_padding[key] - right, self.padding_char
                ).ljust(self.var_padding[key], self.padding_char)
            header += "|" + self.newline_char

        if self.row_sep == "always":
            header += self.var_row_sep + self.newline_char
        if self.row_sep == "markdown":
            header += self.var_row_sep.replace("+", "|") + self.newline_char
        return header

    def get_body(self) -> str:
        """Get the body of the markdown table"""
        rows = ""
        for i, item in enumerate(self._cells):
            rows += self.__get_row(item)
            if i < len(self.data) - 1:
                rows += self.newline_char
            if self.row_sep == "always" and i < len(self.data) - 1:
                rows += self.var_row_sep + self.newline_char
            if self.row_sep in ["topbottom", "always"] and i == len(self.data) - 1:
                rows += self.newline_char + self.var_row_sep_last
        return rows

    def get_markdown(self) -> str:
        """Get the complete markdown table"""
        self.__update_meta_params()
        if not self.multiline:
            self.__reject_line_breaks()
        data = self.get_header() + self.get_body()
        if self.quote:
            return "```" + data + "```"
        return data

# PEP 8 spelling kept as an alias; the lowercase name is what the README and
# every existing caller use, so it stays the primary export.
MarkdownTable = markdown_table
