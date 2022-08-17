# markdownTable
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hvalev/markdownTable/test'n'publish)
[![codecov](https://codecov.io/gh/hvalev/markdownTable/branch/main/graph/badge.svg?token=ZZ8WXO4H6P)](https://codecov.io/gh/hvalev/markdownTable)
[![Downloads](https://pepy.tech/badge/py-markdown-table)](https://pepy.tech/project/py-markdown-table)
[![Downloads](https://pepy.tech/badge/py-markdown-table/month)](https://pepy.tech/project/py-markdown-table)
[![Downloads](https://pepy.tech/badge/py-markdown-table/week)](https://pepy.tech/project/py-markdown-table)

A class used to generate padded tables in a markdown code block. It also works with pandas dataframes.

## Installation
using pip:
```pip install py-markdown-table```
importing:
```from markdownTable import markdownTable```

## Usage
```markdownTable(data).getMarkdown()```
or
```markdownTable(data).setParams(...).getMarkdown()```
where data is a `list` of `dict` where each dict represents a row. Keys must be uniform for all `dict` elements and are used to span the header. Values populate the cells for each row. 
## Parameters
Chaining `.setParams(...)` to a `markdownTable(data)` object allows you to pass the following keyword arguments:

```
|      param      |       type      |     values    |                         description                        |
|-----------------|-----------------|---------------|------------------------------------------------------------|
|     row_sep     |       str       |               |       Row separation strategy using `----` as pattern      |
|                 |                 |     always    |                      Separate each row                     |
|                 |                 |   topbottom   |Separate the top (header) and bottom (last row) of the table|
|                 |                 |    markdown   |               Separate only header from body               |
|                 |                 |      None     |             No row separators will be inserted             |
|  padding_width  |       int       |               |             Allocate padding to all table cells            |
|  padding_weight |       str       |               |     Strategy for allocating padding within table cells     |
|                 |                 |      left     |        Aligns cell's contents to the end of the cell       |
|                 |                 |     right     |     Aligns cell's contents to the beginning of the cell    |
|                 |                 |   centerleft  |         Centers cell's contents with extra padding         |
|                 |                 |               |           allocated to the beginning of the cell           |
|                 |                 |  centerright  |         Centers cell's contents with extra padding         |
|                 |                 |               |              allocated to the end of the cell              |
|   padding_char  |       str       |               |           Single character used to fill extra and          |
|                 |                 |               |           normal padding with. Default is a blank          |
|                 |                 |               |                         space ` `.                         |
|   newline_char  |       str       |               |          Custom character appended to each row to          |
|                 |                 |               |              force a newline. Default is `\n`              |
|  float_rounding |       int       |               |       Keep values up until `float_rounder` after the       |
|                 |                 |               |          decimal dot. Default is `2`, but can also         |
|                 |                 |               |             be set to `None` to not round down             |
|                 |                 |               |                           floats.                          |
|      quote      |       bool      |               |       If `true` (default) wrap the generated markdown      |
|                 |                 |               |                 table with block code quote                |
|    multiline    |  dict<Any,int>  |               |           Predefine the column width by passing a          |
|                 |                 |               |           dict() with keys matching those of the           |
|                 |                 |               |         passed data and values -- the desired width        |
|                 |                 |               |               for each corresponding column.               |
```

## Using it with a dataframe

```
import pandas as pd
from markdownTable import markdownTable

file = 'sample.csv'
df = pd.read_csv(file)
markdownTable(df.to_dict(orient='records')).getMarkdown()
```

## Examples

```markdownTable(data).setParams(row_sep = 'always').getMarkdown()```
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

```markdownTable(data).setParams(row_sep = 'topbottom').getMarkdown()```
```
+----------------------------------------+
|    title   |    time   |   date  |seats|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
+----------------------------------------+
```

```markdownTable(data).setParams(row_sep = 'markdown').getMarkdown()```
```
|    title   |    time   |   date  |seats|
|------------|-----------|---------|-----|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|
```

```markdownTable(data).setParams(row_sep = 'markdown', quote = False).getMarkdown()```

|    title   |    time   |   date  |seats|
|------------|-----------|---------|-----|
|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|
|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|
|Vrij zwemmen| 7:30-8:30 |Fri 11.12|18/18|
|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|


```markdownTable(data).setParams(row_sep = 'topbottom', padding_width = 5, padding_weight='left').getMarkdown()```
```
+------------------------------------------------------------+
|            title|            time|          date|     seats|
|     Vrij Zwemmen|     21:30-23:00|     Wed 09.12|     24/24|
|     Vrij Zwemmen|     12:00-13:00|     Thu 10.12|     18/18|
|     Vrij zwemmen|       7:30-8:30|     Fri 11.12|     18/18|
|     Vrij Zwemmen|     13:15-14:15|     Sat 12.12|     18/18|
+------------------------------------------------------------+
```

```markdownTable(data).setParams(row_sep = 'topbottom', padding_width = 5, padding_weight = 'centerright').getMarkdown()```
```
+------------------------------------------------------------+
|      title      |      time      |     date     |  seats   |
|  Vrij Zwemmen   |  21:30-23:00   |  Wed 09.12   |  24/24   |
|  Vrij Zwemmen   |  12:00-13:00   |  Thu 10.12   |  18/18   |
|  Vrij zwemmen   |   7:30-8:30    |  Fri 11.12   |  18/18   |
|  Vrij Zwemmen   |  13:15-14:15   |  Sat 12.12   |  18/18   |
+------------------------------------------------------------+
```

```mt = markdownTable(data).setParams(row_sep = 'always', padding_width = 5, padding_weight='centerright', padding_char = '.').getMarkdown()```
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
