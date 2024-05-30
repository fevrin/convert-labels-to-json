#!/usr/bin/env python3

import json
import logging
import re
import sys
from collections import deque

def convert_to_json(data):
    """
    Converts a list of lines with multiple key-value pairs to a JSON string.

    Args:
        data: A list of strings, where each string represents a line with key-value pairs.

    Returns:
        A JSON string representing the converted data.
    """

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
                logging.info("skipping char '{0}'".format(char))
                skip_next_char = False
                logging.info("skip_next_char = '{0}'".format(skip_next_char))
                continue

#            if char in special_chars:
#                print(f"special char = '{char}'")
#                print(f"key = '{type(key)}'")


            if key == "":
                if char == '=':
                    key = ''.join(word)
                    word = []
                    logging.info("key = '%s'", key)
                    continue
                else:
                    logging.debug("appending '%s' to key", char)
                    word.append(char)
            else:
                if char in ['\'','"'] and not quote_char:
                    # make note of the quote character and the fact that we're within quotes
                    quote_char = char
                    in_quoted_value = True
                    logging.debug("quote_char = %s", quote_char)
                    logging.debug("in_quoted_value = '%s'", in_quoted_value)
                    continue
                if (quote_char and char == quote_char and word[-1] != '\\') \
                   or (not quote_char and char == ' '):
                    # we're at the end of the value, either:
                    # * we're within quotes and are now exiting those
                    # * the value wasn't quoted, and we're now at the end of the unquoted value
                    value = ''.join(word)
                    logging.info("word[-1] = %s", word[-1])
                    logging.info("value = '%s'", value)

                    key_values[key] = value
                    logging.info("key_values['{}'] = '{}'".format(key, value))
                    logging.info("found both key and value; moving to next pair")

                    # reset variables in preparation for the next key-value pair
                    key, value = "", ""
                    in_quoted_value = False
                    quote_char = None
                    word = []

                    if char != ' ':
                        # if the current character isn't a space (e.g., it's a quote), don't
                        # include the following character (should be a space) in the value
                        skip_next_char = True

                    logging.debug("skip_next_char = '%s'", skip_next_char)
                    logging.info("\n")
                else:
                    logging.debug("appending '%s' to value", char)
                    word.append(char)

        error_list.append(key_values)
        key_values = {}

        logging.info("found all keys and values on line; moving to next line")
        logging.info("\n\n")

    error_list.append({"error summary": error_summary})
    return error_list

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL, style='{')

    # Get filename from command line argument (optional)
    if len(sys.argv) > 1:
      data = sys.argv[1]
      # Open file in read mode (code remains the same)
      with open(data, 'r') as f:
        lines = f.readlines()
    else:
      # Read lines from standard input
      lines = sys.stdin.readlines()

    # Convert lines to JSON string
    json_data = convert_to_json(lines)

    # Print the JSON string
    logging.debug("error_list = '%s'", json.dumps(json_data, indent=4))
    print(json.dumps(json_data, indent=4))
