#!/usr/bin/env python3

import json
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
    key_values = {}
    for line in lines:
        line_dict = {}
        current_key = None
        current_value = deque()  # Use deque for handling quoted values
        in_quoted_value = False
        skip_next_char = False

        word = []
        key = ""
        value = ""
        for char in line:
#            print(f"char = '{char}'")
            if skip_next_char is True:
                skip_next_char = False
                print(f"skip_next_char = '{skip_next_char}' ({char})")
                continue
            if char in special_chars:
                print(f"special char = '{char}'")
#                print(f"key = '{type(key)}'")
                if char == '=':
                    if key == "":
                        key = ''.join(word)
                        word = []
                        print(f"key = '{key}'")
                    else:
                        value = ''.join(word)
                        print(f"value = '{value}'")
                if char == '"':
                    if in_quoted_value == False:
                        if word[:-1] != '\\':
                            in_quoted_value = True
                    else:
                        if word[:-1] != '\\':
                            # assign the current set of characters to value'
                            value = ''.join(word)
                            key_values[key] = value

                            # reset variables in preparation for the next key-value pair
                            key, value = "", ""
                            in_quoted_value = False
                            skip_next_char = True
                            word = []
                            print(f"skip_next_char = '{skip_next_char}'")

                    print(f"in_quoted_value = '{in_quoted_value}'")
            else:
                if key == "":
                    print(f"appending '{char}' to key")
                    word.append(char)
                else:
                    print(f"appending '{char}' to value")
                    word.append(char)

    print(f"key_values = '{json.dumps(key_values, indent=4)}'")


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
