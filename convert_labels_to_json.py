#!/usr/bin/env python3

import json
import re
import sys
from collections import deque

def convert_to_json_orig(data):
    """
    Converts a list of lines with multiple key-value pairs to a JSON string.

    Args:
        data: A list of strings, where each string represents a line with key-value pairs.

    Returns:
        A JSON string representing the converted data.
    """

    if data == '-':
      # Read lines from standard input
      lines = sys.stdin.readlines()
    else:
      # Open file in read mode (code remains the same)
      with open(data, 'r') as f:
        lines = f.readlines()

    result = []
    for line in lines:
        line_dict = {}
        current_key = None
        current_value = deque()  # Use deque for handling quoted values
        in_quoted_value = False

        for token in line.strip().split():
            print(f"token = '{token}'")

            if "=" in token:
                # Split key-value pair
                key, value = token.split("=", 1)
                current_key = key.strip()  # Preserve potential leading/trailing spaces in key
                # Clear current value if a new key is encountered
                current_value.clear()
                in_quoted_value = False
            else:
                # Handle quoted values
                if token.startswith('"'):
                    in_quoted_value = True
                    current_value.append(token[1:])  # Add first part without quotes
                elif token.endswith('"'):
                    in_quoted_value = False
                    current_value.append(token[:-1])  # Add last part without quotes
                else:
                    # Handle non-quoted values or continuation within quotes
                    if in_quoted_value:
                        current_value.append(token)
                    else:
                        current_value.append(token.strip())  # Handle leading spaces outside quotes

            # Add complete key-value pair to dictionary
            if current_key and current_value:
                line_dict[current_key] = " ".join(current_value)

        if current_key and current_value:
            # Add the last key-value pair if any
            line_dict[current_key] = " ".join(current_value)
        result.append(line_dict)
    return json.dumps(result, indent=4)

def convert_to_json(data):
    """
    Converts a list of lines with multiple key-value pairs to a JSON string.

    Args:
        data: A list of strings, where each string represents a line with key-value pairs.

    Returns:
        A JSON string representing the converted data.
    """

    if data == '-':
      # Read lines from standard input
      lines = sys.stdin.readlines()
    else:
      # Open file in read mode (code remains the same)
      with open(data, 'r') as f:
        lines = f.readlines()

    result = []
    special_chars = ['\'','"','\\','=','\n']
    error_list = []
    key_values = {}
    error_summary = ""
    for line in lines:
        line = line.strip()
        line_dict = {}
        current_key = None
        current_value = deque()  # Use deque for handling quoted values
        in_quoted_value = False
        skip_next_char = False
        quote_char = None

        word = []
        key = ""
        value = ""
        if re.match("^[^:]+: error:", line):
            error_summary = line
            continue

        for char in line:
#            print(f"char = '{char}'")
            if skip_next_char is True:
                print(f"skipping char '{char}'")
                skip_next_char = False
                print(f"skip_next_char = '{skip_next_char}'")
                continue

#            if char in special_chars:
#                print(f"special char = '{char}'")
#                print(f"key = '{type(key)}'")


            if key == "":
                if char == '=':
                    key = ''.join(word)
                    word = []
                    print(f"key = '{key}'")
                    continue
                else:
                    print(f"appending '{char}' to key")
                    word.append(char)
            else:
                if char in ['\'','"'] and not quote_char:
                    quote_char = char
                    in_quoted_value = True
                    print(f"quote_char = {quote_char}")
                    print(f"in_quoted_value = '{in_quoted_value}'")
                    continue
                if (quote_char and char == quote_char and word[-1] != '\\') \
                   or (not quote_char and char == ' '):
                    value = ''.join(word)
                    print(f"word[-1] = {word[-1]}")
                    print(f"value = '{value}'")

                    key_values[key] = value
                    print(f"key_values[{key}] = {value}")
                    print("found both key and value; moving to next pair")

                    # reset variables in preparation for the next key-value pair
                    key, value = "", ""
                    in_quoted_value = False
                    quote_char = None
                    word = []

                    if char != ' ':
                        skip_next_char = True

                    print(f"skip_next_char = '{skip_next_char}'")
                    print()
                else:
                    print(f"appending '{char}' to value")
                    word.append(char)

        error_list.append(key_values)
        key_values = {}

    error_list.append({"error summary": error_summary})
    print(f"error_list = '{json.dumps(error_list, indent=4)}'")

if __name__ == "__main__":
    # Get filename from command line argument (optional)
    if len(sys.argv) > 1:
      data = sys.argv[1]
    else:
      # Use standard input (default)
      data = '-'

    # Convert lines to JSON string
    json_data = convert_to_json(data)

    # Print the JSON string
    print(json_data)
