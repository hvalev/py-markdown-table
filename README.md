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

## Parameters
The library supports has the following parameters:
```
markdownTable(data):
    data (list): List of dicts with uniform {key : value} pairs used to generate the header
markdownTable(data).setParams(...):
    row_sep (str): Row separation strategy with the following options:
            'always'        Separate each row
            'topbottom'     Insert row separator above header and below the last row
            'markdown'      Single header/body separator formated as valid markdown
            'None'          No row separation
    padding_width (int):    Extra padding to all table cells
    padding_weight (str):   Padding strategy. The following values are accepted:
            'left'          Aligns items to the end of the cell
            'right'         Aligns items to the beginning of the cell
            'centerleft'    Centers items, where extra padding is allocated to the beginning of the cell
            'centerright'   Centers items, where extra padding is allocated to the end of the cell
    padding_char (str):     Custom single character to fill extra and normal padding with. Default is a blank space.
    newline_char (str):     Custom character to be used for indicating a newline. Default is '\n'
    float_rounding (int):   Round down float values to a number decimal places.
                            Default is 2, but can also be set to 'None' to not round down.
    quote(bool):            If true (default) surrounds the table with markdown block code quote
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
