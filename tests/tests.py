import pytest
from markdownTable import markdownTable


bad_data_0 = []

bad_data_1 = [{'one': 'two', 'three': 'four'},
              {'one': 'two'}]

bad_data_2 = [{'one': 'two', 'three': 'four'},
              {'one': 'two', 'four': 'three'}]

formatting_data = [{'title': 'Vrij Zwemmen', 'time': '21:30-23:00', 'date': 'Wed 09.12', 'seats': '24/24'},
                   {'title': 'Vrij Zwemmen', 'time': '12:00-13:00', 'date': 'Thu 10.12', 'seats': '18/18'},
                   {'title': 'Vrij Zwemmen', 'time': '7:30-8:30', 'date': 'Fri 11.12', 'seats': '18/18'},
                   {'title': 'Vrij Zwemmen', 'time': '13:15-14:15', 'date': 'Sat 12.12', 'seats': '18/18'}]

multiline_data = [{"A": "row1_A and additional stuff", "B": "row1_B", "C": "row1_C"},
                  {"A": "row2_A", "B": "row2_B and additional stuff", "C": "row2_C"},
                  {"A": "row3_A", "B": "row3_B", "C": "row3_C"}]

def test_bad_data_missing_data():
    with pytest.raises(Exception):
        markdownTable(bad_data_0).getMarkdown()


def test_bad_data_missing_key():
    with pytest.raises(Exception):
        markdownTable(bad_data_1).getMarkdown()


def test_bad_data_non_uniform_key():
    with pytest.raises(Exception):
        markdownTable(bad_data_2).getMarkdown()


def test_formatting_plain():
    mt = markdownTable(formatting_data).getMarkdown()
    res = '```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```'
    assert mt == res


def test_formatting_topbottom():
    mt = markdownTable(formatting_data).setParams(row_sep='topbottom').getMarkdown()
    res = '```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```'
    assert mt == res


def test_formatting_markdown():
    mt = markdownTable(formatting_data).setParams(row_sep='markdown').getMarkdown()
    res = '```|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|```'
    assert mt == res


def test_formatting_markdown_noquote():
    mt = markdownTable(formatting_data).setParams(row_sep='markdown', quote=False).getMarkdown()
    res = '|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|'
    assert mt == res


def test_formatting_right():
    mt = markdownTable(formatting_data).setParams(row_sep='topbottom', padding_weight='right').getMarkdown()
    res = '```\n+----------------------------------------+\n|title       |time       |date     |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen|7:30-8:30  |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```'
    assert mt == res


def test_formatting_padding1():
    mt = markdownTable(formatting_data).setParams(row_sep='topbottom', padding_width=5, padding_weight='left').getMarkdown()
    res = '```\n+------------------------------------------------------------+\n|            title|            time|          date|     seats|\n|     Vrij Zwemmen|     21:30-23:00|     Wed 09.12|     24/24|\n|     Vrij Zwemmen|     12:00-13:00|     Thu 10.12|     18/18|\n|     Vrij Zwemmen|       7:30-8:30|     Fri 11.12|     18/18|\n|     Vrij Zwemmen|     13:15-14:15|     Sat 12.12|     18/18|\n+------------------------------------------------------------+```'
    assert mt == res


def test_formatting_padding2():
    mt = markdownTable(formatting_data).setParams(row_sep='topbottom', padding_width=5, padding_weight='centerright').getMarkdown()
    res = '```\n+------------------------------------------------------------+\n|      title      |      time      |     date     |  seats   |\n|  Vrij Zwemmen   |  21:30-23:00   |  Wed 09.12   |  24/24   |\n|  Vrij Zwemmen   |  12:00-13:00   |  Thu 10.12   |  18/18   |\n|  Vrij Zwemmen   |   7:30-8:30    |  Fri 11.12   |  18/18   |\n|  Vrij Zwemmen   |  13:15-14:15   |  Sat 12.12   |  18/18   |\n+------------------------------------------------------------+```'
    assert mt == res


def test_formatting_padding_char():
    mt = markdownTable(formatting_data).setParams(row_sep='always', padding_width=5, padding_weight='centerright', padding_char='.').getMarkdown()
    res = '```\n+------------------------------------------------------------+\n|......title......|......time......|.....date.....|..seats...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..21:30-23:00...|..Wed 09.12...|..24/24...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..12:00-13:00...|..Thu 10.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|...7:30-8:30....|..Fri 11.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..13:15-14:15...|..Sat 12.12...|..18/18...|\n+------------------------------------------------------------+```'
    assert mt == res

def test_multiline_data():
    mt = markdownTable(multiline_data).setParams(padding_width=2,padding_weight="centerleft",multiline=True).getMarkdown()
    res = '```\n+----------------------------------+\n|      A     |      B     |    C   |\n+------------+------------+--------+\n| row1_A and |   row1_B   | row1_C |\n| additional |            |        |\n|    stuff   |            |        |\n+------------+------------+--------+\n|   row2_A   | row2_B and | row2_C |\n|            | additional |        |\n|            |    stuff   |        |\n+------------+------------+--------+\n|   row3_A   |   row3_B   | row3_C |\n+----------------------------------+```'
    assert mt == res
