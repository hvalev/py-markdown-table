# markdownTable

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hvalev/markdownTable/test?label=test)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hvalev/markdownTable/deploy?label=deploy)
[![codecov](https://codecov.io/gh/hvalev/markdownTable/branch/main/graph/badge.svg?token=ZZ8WXO4H6P)](https://codecov.io/gh/hvalev/markdownTable)
[![HitCount](http://hits.dwyl.com/hvalev/markdownTable.svg)](http://hits.dwyl.com/hvalev/markdownTable)

A class used to generate padded tables in a markdown code block. It also works with pandas dataframes.

# Installation
using pip:
```pip install py-markdown-table```
importing:
```from markdownTable import markdownTable```

# Parameters
The library supports has the following parameters:
```
row_sep = 'always'                  -> strategy for row separation
padding_width = 0                   -> additional character width to pad table cells with
padding_weight = 'centerleft'       -> strategy for allocating extra padding in cells
padding_char = ' '                  -> filler character for padding
newline_char = '\n'                 -> newline character to use
float_rounding = 2                  -> round to decimal point for float values
```

Parameters can be set with the setParams() function:
markdownTable(t).setParams(float_rounding = 2, padding_char = '.')

# Examples with DataFrames

```
import pandas as pd
from markdownTable import markdownTable

file = 'sample.csv'
df = pd.read_csv(file)
markdownTable(df.to_dict(orient='records')).getMarkdown()
```

# Examples Plain

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
