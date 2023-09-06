import re
from metadata_functions import use_message_meta

"""
Text Encode and Decode
"""


def text_encode(text_file_path, binary_message, output_path):
    # read contents of text file
    with open(text_file_path, "r") as file:
        original_text = file.read()

    # Alter text such that there are no consecutive spaces
    modified_text = re.sub(r' +', ' ', original_text)

    # Count the number of spaces in the text
    space_count = original_text.count(" ")

    if space_count < len(binary_message):
        raise ValueError('Message is too large to be encoded in the text file')

    bit_pointer = 0
    space_pointer = 0

    while bit_pointer < len(binary_message):
        while modified_text[space_pointer] != " ":
            space_pointer += 1

        # If bit is 1, add a double space
        if binary_message[bit_pointer] == "1":
            modified_text = modified_text[:space_pointer] + "  " + modified_text[space_pointer + 1:]
            space_pointer += 2
            bit_pointer += 1

        # If bit is 0, maintain single space
        elif binary_message[bit_pointer] == "0":
            space_pointer += 1
            bit_pointer += 1

    with open(output_path, "w") as file:
        file.write(modified_text)

    print("message encoded to text successfully")


def text_decode(encoded_text_path):
    # read contents of text file
    with open(encoded_text_path, "r") as file:
        encoded_text = file.read()

    space_pointer = 0
    binary_message = ""

    while space_pointer < len(encoded_text):
        while space_pointer < len(encoded_text) and encoded_text[space_pointer] != " ":
            space_pointer += 1

        # if double space is encountered, the bit is 1
        if encoded_text[space_pointer: space_pointer + 2] == "  ":
            binary_message += "1"
            space_pointer += 2

        # if single space is encountered, the bit is 0
        else:
            binary_message += "0"
            space_pointer += 1

    # Get meta data from the binary sequence
    binary_message, ext = use_message_meta(binary_message)

    return binary_message, ext
