# pylint: skip-file
import string
import random
import time
from py_markdown_table.markdown_table import markdown_table
from py_markdown_table.utils import find_longest_contiguous_strings


def generate_dict_list(num_keys, num_dicts, values_length, include_whitespace=False):
    dict_list = []
    keys = [f"key{i}" for i in range(1, num_keys + 1)]
    for _ in range(num_dicts):
        dictionary = {}
        for key in keys:
            value = "".join(
                random.choice(string.ascii_letters + string.digits + " ")
                for _ in range(values_length)
            )
            dictionary[key] = value
        dict_list.append(dictionary)
    return dict_list


# Define the parameter ranges
num_keys_range = [2, 4, 8, 16]
num_dicts_range = [10, 40, 160, 640]
values_length_range = [5, 20, 80, 320]
include_whitespace_range = [False, False, True, True]

# num_keys_range = [3]
# num_dicts_range = [2]
# values_length_range = [40]
# include_whitespace_range = [True]

# Create a list to store the sampled parameter combinations
parameter_combinations = []

# Iterate over the parameter ranges
for i in range(4):
    num_keys = num_keys_range[i]
    num_dicts = num_dicts_range[i]
    values_length = values_length_range[i]
    include_whitespace = include_whitespace_range[i]

    # Generate the dictionary list for the current parameter combination
    dictionary_list = generate_dict_list(
        num_keys, num_dicts, values_length, include_whitespace
    )

    # Store the parameter combination and the generated dictionary list
    parameter_combinations.append(
        {
            "num_keys": num_keys,
            "num_dicts": num_dicts,
            "values_length": values_length,
            "include_whitespace": include_whitespace,
            "dictionary_list": dictionary_list,
        }
    )


def create_benchmark(columns, rows, cell_length, multiline, speed):
    return {
        "parameters": f"columns: {columns}~rows: {rows}~cell_size: {cell_length}",
        "Multiline": str(multiline),
        "speed": f"{str('{:.6f}'.format(speed))} ms",
    }


# find biggest contiguous string in the elements of a list of dicts
results = []

print("########### without multiline ##############")
# Print the sampled parameter combinations without multiline
for params in parameter_combinations:
    print("Parameter Combination:")
    print(f"columns: {params['num_keys']}")
    print(f"rows: {params['num_dicts']}")
    print(f"cell_value_length: {params['values_length']}")
    # print(f"include_whitespace: {params['include_whitespace']}")
    # print(f"dictionary_list: {params['dictionary_list']}")

    start_time = time.time() * 1000
    markdown_table(params["dictionary_list"]).set_params(
        padding_width=0, padding_weight="centerleft"
    ).get_markdown()
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    print(f"Benchmark - Elapsed Time: {elapsed_time} milliseconds")
    results.append(
        create_benchmark(
            params["num_keys"],
            params["num_dicts"],
            params["values_length"],
            False,
            elapsed_time,
        )
    )

print("########### with multiline ##############")
# Print the sampled parameter combinations with multiline
for params in parameter_combinations:
    print("Parameter Combination:")
    print(f"columns: {params['num_keys']}")
    print(f"rows: {params['num_dicts']}")
    print(f"cell_value_length: {params['values_length']}")
    # print(f"include_whitespace: {params['include_whitespace']}")
    # print(f"dictionary_list: {params['dictionary_list']}")

    start_time = time.time() * 1000
    res = find_longest_contiguous_strings(params["dictionary_list"])
    markdown_table(params["dictionary_list"]).set_params(
        padding_width=0, padding_weight="centerleft", multiline=res
    ).get_markdown()
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    print(f"Benchmark - Elapsed Time: {elapsed_time} milliseconds")
    results.append(
        create_benchmark(
            params["num_keys"],
            params["num_dicts"],
            params["values_length"],
            True,
            elapsed_time,
        )
    )

print(results)
res = find_longest_contiguous_strings(results, delimiter="~")
benchmark = (
    markdown_table(results)
    .set_params(
        padding_width=2,
        padding_weight="centerleft",
        multiline=res,
        multiline_delimiter="~",
    )
    .get_markdown()
)
print(benchmark)
