# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

Releases before 2.0.0 predate this file; see the [tags](../../tags) and the release notes on
GitHub for those.

## [2.0.0] - 2026-10-21

Everything merged since 1.3.0 (2025-02-06).

### Breaking

- Python 3.8 and 3.9 are dropped; `requires-python` is `>=3.10` (#41).
- A width given to `multiline` is the space left for content, and `padding_width` is added on top
  of it. Before, the two were compared against the whole column, so the same value wrapped at
  `padding_width=0` and silently overran its column at any larger padding (#45).
- Nothing is written back into the caller's objects. `set_params()` and `get_markdown()` used to
  mutate the `data` rows and the `multiline`, `padding_width` and `padding_weight` dictionaries
  passed in, and re-widened the columns on every call, so rendering the same object twice produced
  a different table each time (#43).
- Values that are not strings are rendered as strings in every mode. `multiline` and
  `emoji_spacing="mono"` used to raise `AttributeError` or `TypeError` on an `int`, `float` or
  `None` cell, while the plain path accepted them (#43).
- Option values that cannot be honoured raise `ValueError` naming the offender instead of
  producing a broken table (#43, #45, #49):
  - a per-column `padding_width`, `padding_weight` or `multiline` dict whose keys are not exactly
    the columns of the data, previously `KeyError: 'col'`;
  - `padding_char` given a dict, previously accepted and ignored;
  - `float_rounding` below zero, which rounded floats to tens;
  - a column name wider than the column it names under `multiline_strategy="rows"`, previously
    written past the border;
  - a word wider than its `multiline` column, which could also spin the wrapping loop forever;
  - a line break in a value whose column has no `multiline` width, previously split across two
    output lines.
- `\r\n` and a lone `\r` inside a value are normalised to `\n`, so a line break means a line break
  whichever platform produced the data (#49).
- `from py_markdown_table import markdown_table` yields the class; it used to yield the submodule
  of the same name (#43).

### Added

- `compact` option, which emits the smallest table that is still valid markdown - no padding and
  one `-` per column in the separator - for output that has to fit a size limit (#50, closes #24).
- Every function in the package is annotated and a `py.typed` marker is shipped, so type checkers
  see the real signature of `data` and `set_params` (#51, closes #26).
- `MarkdownTable` as the PEP 8 spelling of the class name; the lowercase name stays primary (#43).
- Test suite from 18 to 177 tests, coverage 86% to 95%, including the invariant that a rendered
  table is a rectangle, and `mypy` in CI (#44, #46, #51).

### Changed

- `emoji_spacing="mono"` decides what is two columns wide from `unicodedata.east_asian_width`
  instead of twelve hand-maintained code point ranges (#48, closes #20). Arrows, dingbats and
  misc symbols (`→ ★ ☀ ✓`) are no longer widened, astral emoji outside the old ranges are,
  a base character followed by U+FE0F is counted, and CJK is padded correctly.
- Packaging and publishing use `uv` instead of Poetry (#32), coverage is collected on every push
  rather than only on tags (#35), and the CI matrix covers 3.10 through 3.15 (#33).
- A custom `multiline_delimiter` is used when rejoining wrapped text; the wrapper used to insert a
  space regardless of the delimiter (#45).
- The README's keyword table and every shown example output are generated from the code, and the
  examples define the data they render (#47, #53).

### Fixed

- `utils/benchmark.py` sized its columns from cell values only, so the header was written past the
  border; `include_header` is now passed (#53).
- The `.venv` entry restored in `.gitignore` (#38), and the status badge pointed at the workflow
  that actually runs (#36).

[2.0.0]: https://github.com/hvalev/py-markdown-table/compare/v1.3.0...v2.0.0
