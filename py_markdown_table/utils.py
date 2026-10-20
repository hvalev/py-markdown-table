"""Util functions which may be used outside of the class for convenience"""
import unicodedata
from typing import Any, Sequence, TypeVar, overload

_EMOJI_PRESENTATION = "\ufe0f"


def count_emojis(text: str) -> list[dict[str, Any]]:
    """Report the characters in a string that a monospace font draws two columns wide.

    That covers emoji in emoji presentation and any other East Asian Wide
    character, CJK among them, so a table of mixed script is padded correctly.
    The widths come from `unicodedata`, which ships with python, so no external
    dependency is involved.

    Args:
        text (str): the string to scan.

    Returns:
        List[Dict]: one entry per wide character, in order of appearance, with
            its `index` in the string, its `value`, and the `spacing` it
            occupies. Sequences assembled from several code points - flags,
            keycaps, ZWJ sequences - yield one entry per code point, so their
            width is over-estimated rather than silently too narrow.
    """
    return [
        {"index": index, "value": char, "spacing": 2}
        for index, char in enumerate(text)
        if _is_double_width(text, index)
    ]


def _is_double_width(text: str, index: int) -> bool:
    if unicodedata.east_asian_width(text[index]) in ("W", "F"):
        return True
    # U+FE0F asks for emoji presentation, which is drawn two columns wide even
    # when the base character on its own is not.
    return index + 1 < len(text) and text[index + 1] == _EMOJI_PRESENTATION


def find_longest_contiguous_strings(
    data: list[dict[str, Any]], include_header: bool = False, delimiter: str = " "
) -> dict[str, int]:
    """Finds the longest contiguous strings in a list of dicts.

    Args:
        data (List[Dict]): List of dicts containing the data to be rendered in a markdown table.
            See markdown_table object description.
        include_header (bool, optional): True if also headers should be parsed. Defaults to False.
        delimiter (str, optional): Which delimiter character to use when splitting a cell's contents.
                                   Defaults to " ".

    Returns:
        Dict: Dictionary containing the minimal width of each column for the input data with keys
              corresponding to the table headers
    """
    longest_strings = {}
    if include_header:
        longest_strings = {key: len(key) for key in data[0].keys()}
    for dictionary in data:  # pylint: disable=R1702
        for key, value in dictionary.items():
            if isinstance(value, str):
                max_length = 0
                current_length = 0
                for char in value:
                    if char != delimiter:
                        current_length += 1
                        if current_length > max_length:
                            max_length = current_length
                    else:
                        current_length = 0
                if max_length > longest_strings.get(key, 0):
                    longest_strings[key] = max_length
    return longest_strings


T = TypeVar("T")


@overload
def split_list_by_indices(sequence: str, indices: Sequence[int]) -> list[str]: ...


@overload
def split_list_by_indices(sequence: list[T], indices: Sequence[int]) -> list[T]: ...


def split_list_by_indices(sequence: Sequence[Any], indices: Sequence[int]) -> list[Any]:
    """Split a sequence at the given positions, keeping them.

    Called with a string and the offsets of its wide characters, so that the
    text between them comes back as separate pieces. An index of 0 yields an
    empty leading piece.

    Args:
        sequence: the sequence to split.
        indices: positions to cut at, ascending.

    Returns:
        The pieces, one more than the number of indices.
    """

    split_list = []
    start = 0
    for index in indices:
        split_list.append(sequence[start:index])
        start = index
    split_list.append(sequence[start:])
    return split_list
