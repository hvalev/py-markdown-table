# py-markdown-table
[![build](https://github.com/hvalev/py-markdown-table/actions/workflows/build.yml/badge.svg)](https://github.com/hvalev/py-markdown-table/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/hvalev/py-markdown-table/branch/main/graph/badge.svg?token=ZZ8WXO4H6P)](https://codecov.io/gh/hvalev/py-markdown-table)
[![Downloads](https://static.pepy.tech/badge/py-markdown-table)](https://pepy.tech/project/py-markdown-table)
[![Downloads](https://static.pepy.tech/badge/py-markdown-table/month)](https://pepy.tech/project/py-markdown-table)
[![Downloads](https://static.pepy.tech/badge/py-markdown-table/week)](https://pepy.tech/project/py-markdown-table)

Tiny python library with zero dependencies which generates formatted multiline tables in `markdown`.

## Basic Use
Install via pip as follows: ```pip install py-markdown-table```

Pass a `list` of `dict`s where the `dict`s must have uniform keys which serve as column headers and the values are expanded to be rows. Simple example with no special formatting:
```
from py_markdown_table.markdown_table import markdown_table
data = [
    {
        "Product": "Smartphone",
        "Brand": "Apple",
        "Price": 999.99
    },
    {
        "Product": "Laptop",
        "Brand": "Dell",
        "Price": 1299.99
    }
]
markdown = markdown_table(data).get_markdown()
print(markdown)
```

```
+------------------------+
|  Product |Brand| Price |
+----------+-----+-------+
|Smartphone|Apple| 999.99|
+----------+-----+-------+
|  Laptop  | Dell|1299.99|
+------------------------+
```

A more comprehensive example showcasing some of the formatting options:
```
from py_markdown_table.markdown_table import markdown_table
jokes_list = [
    {
        "joke1": "Why don't scientists trust atoms? Because they make up everything!",
        "joke2": "Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them!",
        "joke3": "Why don't skeletons fight each other? They don't have the guts!"
    },
    {
        "joke1": "What do you call a snowman with a six-pack? An abdominal snowman!",
        "joke2": "Why don't eggs tell jokes? Because they might crack up!",
        "joke3": "How does a penguin build its house? Igloos it together!"
    }
]
markdown = markdown_table(jokes_list).set_params(padding_width = 3,
                                                 padding_weight = 'centerleft',
                                                 multiline = {'joke1': 30, 'joke2': 30, 'joke3': 30}
                                                 ).get_markdown()
```
```
+--------------------------------------------------------------------------------------------------------------+
|                joke1               |                joke2               |                joke3               |
+------------------------------------+------------------------------------+------------------------------------+
|  Why don't scientists trust atoms? |       Did you hear about the       |   Why don't skeletons fight each   |
|  Because they make up everything!  |    mathematician who's afraid of   |  other? They don't have the guts!  |
|                                    |  negative numbers? He will stop at |                                    |
|                                    |       nothing to avoid them!       |                                    |
+------------------------------------+------------------------------------+------------------------------------+
|  What do you call a snowman with a |     Why don't eggs tell jokes?     |    How does a penguin build its    |
|   six-pack? An abdominal snowman!  |    Because they might crack up!    |     house? Igloos it together!     |
+--------------------------------------------------------------------------------------------------------------+
```

You can also use pandas dataframes by formatting them as follows:
```
from py_markdown_table.markdown_table import markdown_table
data = df.to_dict(orient='records')
markdown_table(data).get_markdown()
```

## Advanced Use
To add parameters to how the markdown table is formatted, you can use the `set_params()` function on a `markdown_table` object, i.e. `markdown_table(data).set_params(...).get_markdown()`, which allows you to pass the following keyword arguments:

```
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
|                       |                     |                   |              `\n`              |
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
```
## Utils
The namespace `py_markdown_table.utils` provides the functions `count_emojis()` and `find_longest_contiguous_strings()`. `count_emojis()` detects emojis and their position in a given string, and `find_longest_contiguous_strings()` finds the longest continuous strings present in the rows and/or columns of your input data. `find_longest_contiguous_strings()` can be useful to figure out the minimal width of each column given a particular data.

## Further Examples
```markdown_table(data).set_params(row_sep = 'always').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
+----------------------------------------+
|    title   |    time   |   date  |seats|
+------------+-----------+---------+-----+
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
+------------+-----------+---------+-----+
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
+------------+-----------+---------+-----+
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
+------------+-----------+---------+-----+
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
+----------------------------------------+
```
</details>
<br/>

```markdown_table(data).set_params(row_sep = 'topbottom').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
+----------------------------------------+
|    title   |    time   |   date  |seats|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
+----------------------------------------+
```
</details>
<br/>

```markdown_table(data).set_params(row_sep = 'markdown').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
|    title   |    time   |   date  |seats|
|------------|-----------|---------|-----|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
```
</details>
<br/>


```markdown_table(data).set_params(row_sep = 'markdown', quote = False).get_markdown()```
<details>
    <summary >
    see example
    </summary>

|    title   |    time   |   date  |seats|
|------------|-----------|---------|-----|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
</details>
<br/>



```markdown_table(data).set_params(row_sep = 'topbottom', padding_width = 5, padding_weight = 'left').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
+------------------------------------------------------------+
|            title|            time|          date|     seats|
|     Vrij Zwemmen|     21:30-23:00|     Wed 09.12|     24/24|
|     Vrij Zwemmen|     12:00-13:00|     Thu 10.12|     18/18|
|     Vrij zwemmen|       7:30-8:30|     Fri 11.12|     18/18|
|     Vrij Zwemmen|     13:15-14:15|     Sat 12.12|     18/18|
+------------------------------------------------------------+
```
</details>
<br/>


```markdown_table(data).set_params(row_sep = 'topbottom', padding_width = 5, padding_weight = 'centerright').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
+------------------------------------------------------------+
|      title      |      time      |     date     |  seats   |
|  Vrij Zwemmen   |  21:30-23:00   |  Wed 09.12   |  24/24   |
|  Vrij Zwemmen   |  12:00-13:00   |  Thu 10.12   |  18/18   |
|  Vrij zwemmen   |   7:30-8:30    |  Fri 11.12   |  18/18   |
|  Vrij Zwemmen   |  13:15-14:15   |  Sat 12.12   |  18/18   |
+------------------------------------------------------------+
```
</details>
<br/>


```markdown_table(data).set_params(row_sep = 'always', padding_width = 5, padding_weight = 'centerright', padding_char = '.').get_markdown()```
<details>
    <summary >
    see example
    </summary>

```
+------------------------------------------------------------+
|......title......|......time......|.....date.....|..seats...|
+-----------------+----------------+--------------+----------+
|..Vrij Zwemmen...|..21:30-23:00...|..Wed 09.12...|..24/24...|
+-----------------+----------------+--------------+----------+
|..Vrij Zwemmen...|..12:00-13:00...|..Thu 10.12...|..18/18...|
+-----------------+----------------+--------------+----------+
|..Vrij zwemmen...|...7:30-8:30....|..Fri 11.12...|..18/18...|
+-----------------+----------------+--------------+----------+
|..Vrij Zwemmen...|..13:15-14:15...|..Sat 12.12...|..18/18...|
+------------------------------------------------------------+
```
</details>
<br/>

`markdown_table(data).set_params(padding_width = 0, padding_weight = "centerleft", multiline = {"A": 25, "B": 12, "C": 9}).get_markdown()`
<details>
    <summary >
    see example
    </summary>

```
+------------------------------------------------+
|            A            |      B     |    C    |
+-------------------------+------------+---------+
|  row1_A and additional  |   row1_B   |  row1_C |
|          stuff          |            |         |
+-------------------------+------------+---------+
|          row2_A         | row2_B and |  row2_C |
|                         | additional |         |
|                         |    stuff   |         |
+-------------------------+------------+---------+
|          row3_A         |   row3_B   |  row3_C |
+------------------------------------------------+
```
</details>
<br/>


`markdown_table(data).set_params(padding_width = 2, padding_weight = "centerleft", multiline = {"A": 25, "B": 12, "C": 9}).get_markdown())`
<details>
    <summary >
    see example
    </summary>

```
+------------------------------------------------------------+
|              A              |        B       |      C      |
+-----------------------------+----------------+-------------+
| row1_A and additional stuff |     row1_B     |    row1_C   |
+-----------------------------+----------------+-------------+
|            row2_A           |   row2_B and   |    row2_C   |
|                             |   additional   |             |
|                             |      stuff     |             |
+-----------------------------+----------------+-------------+
|            row3_A           |     row3_B     |    row3_C   |
+------------------------------------------------------------+
```
</details>
<br/>


`markdown_table(data).set_params(row_sep = "always", multiline = {"those are multi rows": 5}, multiline_strategy = "rows_and_header").get_markdown()`
<details>
    <summary >
    see example
    </summary>

```
+-----+
|those|
| are |
|multi|
| rows|
+-----+
| yes |
| they|
| are |
+-----+
|  no |
| they|
| are |
| not |
+-----+
```
</details>
<br/>


`markdown_table(data).set_params(row_sep = "topbottom", emoji_spacing = "mono", multiline = {"title that is maybe too long": 7, "time": 11, "date": 5, "seats": 5,}, multiline_strategy = "rows_and_header").get_markdown()`
<details>
    <summary >
    see example
    </summary>
*Note:* Github's markdown preview does not render emojis as two whole characters, hence the slight offsets in cells containing emojis.

```
+-------------------------------+
| title |    time   | date|seats|
|that is|           |     |     |
| maybe |           |     |     |
|  too  |           |     |     |
|  long |           |     |     |
|  Vrij |21:30-23:00|  😊 |24/24|
|Zwemmen|           |     |     |
|  Vrij |12:00-13:00| Thu |18/18|
|Zwemmen|           |10.12|     |
|  Vrij | 7:30-8:30 | Fri |  😊 |
|Zwemmen|           |11.12|🌍 🎉|
|  Vrij |13:15-14:15| Sat |20/20|
|Zwemmen|           |12.12|     |
|  Vrij | 7:30-8:30 | Fri | asd |
|Zwemmen|           |11.12|  😊-|
|       |           |     | 🌍: |
|       |           |     |  🎉 |
|Zwemmen|13:15-14:15| Sat |20/20|
|       |           |12.12|     |
+-------------------------------+
```

Below is an example from a monospaced terminal, where the table is rendered correctly.

![Table with emoji in terminal](res/table_w_emoji.jpg)
</details>


## Benchmarks
The table below provide some benchmark results, evaluating the performance on data containing incrementally larger number of `columns`, `rows`, and characters in each table cell (i.e. `cell_size`). You can benchmark it on your own system using the script contained within `py_markdown_table/utils/benchmark.py`. Generally, reasonably-sized tables intended to be read by a human can be generated within a millisecond.

<details>
    <summary >
    see benchmark
    </summary>

```
+-----------------------------------------------+
|    parameters    |Multiline|       speed      |
+------------------+---------+------------------+
|    columns: 2    |  False  |    0.000000 ms   |
|     rows: 10     |         |                  |
|   cell_size: 5   |         |                  |
+------------------+---------+------------------+
|    columns: 4    |  False  |    0.000000 ms   |
|     rows: 40     |         |                  |
|   cell_size: 20  |         |                  |
+------------------+---------+------------------+
|    columns: 8    |  False  |    6.999756 ms   |
|     rows: 160    |         |                  |
|   cell_size: 80  |         |                  |
+------------------+---------+------------------+
|    columns: 16   |  False  |  1173.794678 ms  |
|     rows: 640    |         |                  |
|  cell_size: 320  |         |                  |
+------------------+---------+------------------+
|    columns: 2    |   True  |    0.000000 ms   |
|     rows: 10     |         |                  |
|   cell_size: 5   |         |                  |
+------------------+---------+------------------+
|    columns: 4    |   True  |    0.996338 ms   |
|     rows: 40     |         |                  |
|   cell_size: 20  |         |                  |
+------------------+---------+------------------+
|    columns: 8    |   True  |   16.038330 ms   |
|     rows: 160    |         |                  |
|   cell_size: 80  |         |                  |
+------------------+---------+------------------+
|    columns: 16   |   True  |  1448.473633 ms  |
|     rows: 640    |         |                  |
|  cell_size: 320  |         |                  |
+-----------------------------------------------+
```
</details>
