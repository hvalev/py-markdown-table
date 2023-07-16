# pylint: skip-file
import pytest
from py_markdown_table.markdown_table import markdown_table

bad_data_0 = []

bad_data_1 = [{"one": "two", "three": "four"}, {"one": "two"}]

bad_data_2 = [{"one": "two", "three": "four"}, {"one": "two", "four": "three"}]

formatting_data = [
    {
        "title": "Vrij Zwemmen",
        "time": "21:30-23:00",
        "date": "Wed 09.12",
        "seats": "24/24",
    },
    {
        "title": "Vrij Zwemmen",
        "time": "12:00-13:00",
        "date": "Thu 10.12",
        "seats": "18/18",
    },
    {
        "title": "Vrij Zwemmen",
        "time": "7:30-8:30",
        "date": "Fri 11.12",
        "seats": "18/18",
    },
    {
        "title": "Vrij Zwemmen",
        "time": "13:15-14:15",
        "date": "Sat 12.12",
        "seats": "18/18",
    },
]

multiline_data = [
    {"A": "row1_A and additional stuff", "B": "row1_B", "C": "row1_C"},
    {"A": "row2_A", "B": "row2_B and additional stuff", "C": "row2_C"},
    {"A": "row3_A", "B": "row3_B", "C": "row3_C"},
]

multirow_header_data = [
    {"those are multi rows": "yes they are"},
    {"those are multi rows": "no they are not"},
]

emoji_data = [
    {"title": "Vrij Zwemmen", "time": "21:30-23:00", "date": "😊", "seats": "24/24"},
    {
        "title": "Vrij Zwemmen",
        "time": "12:00-13:00",
        "date": "Thu 10.12",
        "seats": "18/18",
    },
    {"title": "Vrij Zwemmen", "time": "7:30-8:30", "date": "Fri 11.12", "seats": "😊🌍🎉"},
    {
        "title": "Vrij Zwemmen",
        "time": "13:15-14:15",
        "date": "Sat 12.12",
        "seats": "20/20",
    },
]

emoji_multiline_data = [
    {
        "title that is maybe too long": "Vrij Zwemmen",
        "time": "21:30-23:00",
        "date": "😊",
        "seats": "24/24",
    },
    {
        "title that is maybe too long": "Vrij Zwemmen",
        "time": "12:00-13:00",
        "date": "Thu 10.12",
        "seats": "18/18",
    },
    {
        "title that is maybe too long": "Vrij Zwemmen",
        "time": "7:30-8:30",
        "date": "Fri 11.12",
        "seats": "😊🌍🎉",
    },
    {
        "title that is maybe too long": "Vrij Zwemmen",
        "time": "13:15-14:15",
        "date": "Sat 12.12",
        "seats": "20/20",
    },
    {
        "title that is maybe too long": "Vrij Zwemmen",
        "time": "7:30-8:30",
        "date": "Fri 11.12",
        "seats": " asd  😊-🌍:🎉",
    },
    {
        "title that is maybe too long": "Zwemmen",
        "time": "13:15-14:15",
        "date": "Sat 12.12",
        "seats": "20/20",
    },
]


def test_bad_data_missing_data():
    with pytest.raises(Exception):
        markdown_table(bad_data_0).get_markdown()


def test_bad_data_missing_key():
    with pytest.raises(Exception):
        markdown_table(bad_data_1).get_markdown()


def test_bad_data_non_uniform_key():
    with pytest.raises(Exception):
        markdown_table(bad_data_2).get_markdown()


def test_formatting_plain():
    mt = markdown_table(formatting_data).get_markdown()
    res = "```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"
    assert mt == res


def test_formatting_topbottom():
    mt = markdown_table(formatting_data).set_params(row_sep="topbottom").get_markdown()
    res = "```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"
    assert mt == res


def test_formatting_markdown():
    mt = markdown_table(formatting_data).set_params(row_sep="markdown").get_markdown()
    res = "```|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|```"
    assert mt == res


def test_formatting_markdown_noquote():
    mt = (
        markdown_table(formatting_data)
        .set_params(row_sep="markdown", quote=False)
        .get_markdown()
    )
    res = "|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|"
    assert mt == res


def test_formatting_right():
    mt = (
        markdown_table(formatting_data)
        .set_params(row_sep="topbottom", padding_weight="right")
        .get_markdown()
    )
    res = "```\n+----------------------------------------+\n|title       |time       |date     |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen|7:30-8:30  |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"
    assert mt == res


def test_formatting_padding1():
    mt = (
        markdown_table(formatting_data)
        .set_params(row_sep="topbottom", padding_width=5, padding_weight="left")
        .get_markdown()
    )
    res = "```\n+------------------------------------------------------------+\n|            title|            time|          date|     seats|\n|     Vrij Zwemmen|     21:30-23:00|     Wed 09.12|     24/24|\n|     Vrij Zwemmen|     12:00-13:00|     Thu 10.12|     18/18|\n|     Vrij Zwemmen|       7:30-8:30|     Fri 11.12|     18/18|\n|     Vrij Zwemmen|     13:15-14:15|     Sat 12.12|     18/18|\n+------------------------------------------------------------+```"
    assert mt == res


def test_formatting_padding2():
    mt = (
        markdown_table(formatting_data)
        .set_params(row_sep="topbottom", padding_width=5, padding_weight="centerright")
        .get_markdown()
    )
    res = "```\n+------------------------------------------------------------+\n|      title      |      time      |     date     |  seats   |\n|  Vrij Zwemmen   |  21:30-23:00   |  Wed 09.12   |  24/24   |\n|  Vrij Zwemmen   |  12:00-13:00   |  Thu 10.12   |  18/18   |\n|  Vrij Zwemmen   |   7:30-8:30    |  Fri 11.12   |  18/18   |\n|  Vrij Zwemmen   |  13:15-14:15   |  Sat 12.12   |  18/18   |\n+------------------------------------------------------------+```"
    assert mt == res


def test_formatting_padding_char():
    mt = (
        markdown_table(formatting_data)
        .set_params(
            row_sep="always",
            padding_width=5,
            padding_weight="centerright",
            padding_char=".",
        )
        .get_markdown()
    )
    res = "```\n+------------------------------------------------------------+\n|......title......|......time......|.....date.....|..seats...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..21:30-23:00...|..Wed 09.12...|..24/24...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..12:00-13:00...|..Thu 10.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|...7:30-8:30....|..Fri 11.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..13:15-14:15...|..Sat 12.12...|..18/18...|\n+------------------------------------------------------------+```"
    assert mt == res


def test_multiline_data():
    mt = (
        markdown_table(multiline_data)
        .set_params(
            padding_width=0,
            padding_weight="centerleft",
            multiline={"A": 25, "B": 12, "C": 9},
        )
        .get_markdown()
    )
    print(mt)
    res = "```\n+------------------------------------------------+\n|            A            |      B     |    C    |\n+-------------------------+------------+---------+\n|  row1_A and additional  |   row1_B   |  row1_C |\n|          stuff          |            |         |\n+-------------------------+------------+---------+\n|          row2_A         | row2_B and |  row2_C |\n|                         | additional |         |\n|                         |    stuff   |         |\n+-------------------------+------------+---------+\n|          row3_A         |   row3_B   |  row3_C |\n+------------------------------------------------+```"
    assert mt == res


def test_multiline_data_with_padding():
    mt = (
        markdown_table(multiline_data)
        .set_params(
            padding_width=2,
            padding_weight="centerleft",
            multiline={"A": 25, "B": 12, "C": 9},
        )
        .get_markdown()
    )
    print(mt)
    res = "```\n+------------------------------------------------------------+\n|              A              |        B       |      C      |\n+-----------------------------+----------------+-------------+\n| row1_A and additional stuff |     row1_B     |    row1_C   |\n+-----------------------------+----------------+-------------+\n|            row2_A           |   row2_B and   |    row2_C   |\n|                             |   additional   |             |\n|                             |      stuff     |             |\n+-----------------------------+----------------+-------------+\n|            row3_A           |     row3_B     |    row3_C   |\n+------------------------------------------------------------+```"
    assert mt == res


def test_multirow_header_data():
    mt = (
        markdown_table(multirow_header_data)
        .set_params(
            row_sep="always",
            multiline={"those are multi rows": 5},
            multiline_strategy="rows_and_header",
        )
        .get_markdown()
    )
    print(mt)
    res = "```\n+-----+\n|those|\n| are |\n|multi|\n| rows|\n+-----+\n| yes |\n| they|\n| are |\n+-----+\n|  no |\n| they|\n| are |\n| not |\n+-----+```"
    assert mt == res


def test_emoji_data():
    mt = (
        markdown_table(emoji_data)
        .set_params(row_sep="topbottom", emoji_spacing="mono")
        .get_markdown()
    )
    res = "```\n+-----------------------------------------+\n|    title   |    time   |   date  | seats|\n|Vrij Zwemmen|21:30-23:00|    😊   | 24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12| 18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|😊🌍🎉|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12| 20/20|\n+-----------------------------------------+```"
    assert mt == res


def test_emoji_multiline_data():
    mt = (
        markdown_table(emoji_multiline_data)
        .set_params(
            row_sep="topbottom",
            emoji_spacing="mono",
            multiline={
                "title that is maybe too long": 7,
                "time": 11,
                "date": 5,
                "seats": 5,
            },
            multiline_strategy="rows_and_header",
        )
        .get_markdown()
    )
    print(mt)
    res = "```\n+-------------------------------+\n| title |    time   | date|seats|\n|that is|           |     |     |\n| maybe |           |     |     |\n|  too  |           |     |     |\n|  long |           |     |     |\n|  Vrij |21:30-23:00|  😊 |24/24|\n|Zwemmen|           |     |     |\n|  Vrij |12:00-13:00| Thu |18/18|\n|Zwemmen|           |10.12|     |\n|  Vrij | 7:30-8:30 | Fri |  😊 |\n|Zwemmen|           |11.12|🌍 🎉|\n|  Vrij |13:15-14:15| Sat |20/20|\n|Zwemmen|           |12.12|     |\n|  Vrij | 7:30-8:30 | Fri | asd |\n|Zwemmen|           |11.12|  😊-|\n|       |           |     | 🌍: |\n|       |           |     |  🎉 |\n|Zwemmen|13:15-14:15| Sat |20/20|\n|       |           |12.12|     |\n+-------------------------------+```"
    assert mt == res


test_multiline_data()
test_multiline_data_with_padding()
test_multirow_header_data()
test_emoji_multiline_data()
