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


@pytest.mark.parametrize("data", [
    (bad_data_0, pytest.raises(ValueError)),
    (bad_data_1, pytest.raises(ValueError)),
    (bad_data_2, pytest.raises(ValueError)),
])
def test_bad_data(data):
    dataset, expected_exception = data
    with expected_exception:
        markdown_table(dataset).get_markdown()


@pytest.mark.parametrize("params, expected_output", [
    ({}, "```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n+------------+-----------+---------+-----+\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"),
    ({"row_sep": "topbottom"}, "```\n+----------------------------------------+\n|    title   |    time   |   date  |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"),
    ({"row_sep": "markdown"}, "```|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|```"),
    ({"row_sep": "markdown", "quote": False}, "|    title   |    time   |   date  |seats|\n|------------|-----------|---------|-----|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|"),
    ({"row_sep": "topbottom", "padding_weight": "right"}, "```\n+----------------------------------------+\n|title       |time       |date     |seats|\n|Vrij Zwemmen|21:30-23:00|Wed 09.12|24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12|18/18|\n|Vrij Zwemmen|7:30-8:30  |Fri 11.12|18/18|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12|18/18|\n+----------------------------------------+```"),
    ({"row_sep": "topbottom", "padding_width": 5, "padding_weight": "left"}, "```\n+------------------------------------------------------------+\n|            title|            time|          date|     seats|\n|     Vrij Zwemmen|     21:30-23:00|     Wed 09.12|     24/24|\n|     Vrij Zwemmen|     12:00-13:00|     Thu 10.12|     18/18|\n|     Vrij Zwemmen|       7:30-8:30|     Fri 11.12|     18/18|\n|     Vrij Zwemmen|     13:15-14:15|     Sat 12.12|     18/18|\n+------------------------------------------------------------+```"),
    ({"row_sep": "topbottom", "padding_width": 5, "padding_weight": "centerright"}, "```\n+------------------------------------------------------------+\n|      title      |      time      |     date     |  seats   |\n|  Vrij Zwemmen   |  21:30-23:00   |  Wed 09.12   |  24/24   |\n|  Vrij Zwemmen   |  12:00-13:00   |  Thu 10.12   |  18/18   |\n|  Vrij Zwemmen   |   7:30-8:30    |  Fri 11.12   |  18/18   |\n|  Vrij Zwemmen   |  13:15-14:15   |  Sat 12.12   |  18/18   |\n+------------------------------------------------------------+```"),
    ({"row_sep": "always", "padding_width": 5, "padding_weight": "centerright", "padding_char": "."}, "```\n+------------------------------------------------------------+\n|......title......|......time......|.....date.....|..seats...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..21:30-23:00...|..Wed 09.12...|..24/24...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..12:00-13:00...|..Thu 10.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|...7:30-8:30....|..Fri 11.12...|..18/18...|\n+-----------------+----------------+--------------+----------+\n|..Vrij Zwemmen...|..13:15-14:15...|..Sat 12.12...|..18/18...|\n+------------------------------------------------------------+```"),
])
def test_formatting(params, expected_output):
    mt = markdown_table(formatting_data).set_params(**params).get_markdown()
    assert mt == expected_output


@pytest.mark.parametrize("params, expected_output", [
    ({"padding_width": 0, "padding_weight": "centerleft", "multiline": {"A": 25, "B": 12, "C": 9}}, "```\n+------------------------------------------------+\n|            A            |      B     |    C    |\n+-------------------------+------------+---------+\n|  row1_A and additional  |   row1_B   |  row1_C |\n|          stuff          |            |         |\n+-------------------------+------------+---------+\n|          row2_A         | row2_B and |  row2_C |\n|                         | additional |         |\n|                         |    stuff   |         |\n+-------------------------+------------+---------+\n|          row3_A         |   row3_B   |  row3_C |\n+------------------------------------------------+```"),
    ({"padding_width": 2, "padding_weight": "centerleft", "multiline": {"A": 25, "B": 12, "C": 9}}, "```\n+------------------------------------------------------------+\n|              A              |        B       |      C      |\n+-----------------------------+----------------+-------------+\n| row1_A and additional stuff |     row1_B     |    row1_C   |\n+-----------------------------+----------------+-------------+\n|            row2_A           |   row2_B and   |    row2_C   |\n|                             |   additional   |             |\n|                             |      stuff     |             |\n+-----------------------------+----------------+-------------+\n|            row3_A           |     row3_B     |    row3_C   |\n+------------------------------------------------------------+```"),
])
def test_multiline_data(params, expected_output):
    mt = markdown_table(multiline_data).set_params(**params).get_markdown()
    assert mt == expected_output


@pytest.mark.parametrize("params, expected_output", [
    ({"row_sep": "always", "multiline": {"those are multi rows": 5}, "multiline_strategy": "rows_and_header"}, "```\n+-----+\n|those|\n| are |\n|multi|\n| rows|\n+-----+\n| yes |\n| they|\n| are |\n+-----+\n|  no |\n| they|\n| are |\n| not |\n+-----+```"),
])
def test_multirow_header_data(params, expected_output):
    mt = markdown_table(multirow_header_data).set_params(**params).get_markdown()
    assert mt == expected_output


@pytest.mark.parametrize("params, expected_output", [
    ({"row_sep": "topbottom", "emoji_spacing": "mono"}, "```\n+-----------------------------------------+\n|    title   |    time   |   date  | seats|\n|Vrij Zwemmen|21:30-23:00|    😊   | 24/24|\n|Vrij Zwemmen|12:00-13:00|Thu 10.12| 18/18|\n|Vrij Zwemmen| 7:30-8:30 |Fri 11.12|😊🌍🎉|\n|Vrij Zwemmen|13:15-14:15|Sat 12.12| 20/20|\n+-----------------------------------------+```"),
])
def test_emoji_data(params, expected_output):
    mt = markdown_table(emoji_data).set_params(**params).get_markdown()
    assert mt == expected_output


@pytest.mark.parametrize("params, expected_output", [
    ({"row_sep": "topbottom", "emoji_spacing": "mono", "multiline": {"title that is maybe too long": 7, "time": 11, "date": 5, "seats": 5}, "multiline_strategy": "rows_and_header"}, "```\n+-------------------------------+\n| title |    time   | date|seats|\n|that is|           |     |     |\n| maybe |           |     |     |\n|  too  |           |     |     |\n|  long |           |     |     |\n|  Vrij |21:30-23:00|  😊 |24/24|\n|Zwemmen|           |     |     |\n|  Vrij |12:00-13:00| Thu |18/18|\n|Zwemmen|           |10.12|     |\n|  Vrij | 7:30-8:30 | Fri |  😊 |\n|Zwemmen|           |11.12|🌍 🎉|\n|  Vrij |13:15-14:15| Sat |20/20|\n|Zwemmen|           |12.12|     |\n|  Vrij | 7:30-8:30 | Fri | asd |\n|Zwemmen|           |11.12|  😊-|\n|       |           |     | 🌍: |\n|       |           |     |  🎉 |\n|Zwemmen|13:15-14:15| Sat |20/20|\n|       |           |12.12|     |\n+-------------------------------+```"),
])
def test_emoji_multiline_data(params, expected_output):
    mt = markdown_table(emoji_multiline_data).set_params(**params).get_markdown()
    assert mt == expected_output

