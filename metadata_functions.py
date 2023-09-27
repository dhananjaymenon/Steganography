import math


def add_frame_meta(binary_sequence_with_meta: str, frame_max: int) -> str:
    """
    Only used for video encoder

    Adds the number of frames in the carrier video that are used
    to the beginning of the binary sequence
    """

    # Length binary = frame_meta + len(binary_sequence_with_meta)
    len_binary = 32 + len(binary_sequence_with_meta)

    number_of_frames = math.ceil(len_binary/frame_max)
    number_of_frames_binary = format(number_of_frames, '032b')

    return number_of_frames_binary+binary_sequence_with_meta


def add_message_meta(binary_sequence: str, ext: str) -> str:
    """
    Adds meta data:
    - length of binary string (32 bits)
    - extension (8 + 8 + 8 bits)
    to the binary sequence and returns binary sequence with the meta-data
    """
    if len(ext) != 3:
        raise Exception("Invalid extension: Only extensions with 3 characters are accepted")

    length = len(binary_sequence)

    length_binary = format(length, '032b')
    ext_binary = format(ord(ext[0]), '08b') + format(ord(ext[1]), '08b') + format(ord(ext[2]), '08b')

    return length_binary+ext_binary+binary_sequence


def use_message_meta(long_binary_sequence: str) -> (str, str):
    """
    Finds the binary sequence and extension of secret media file
    from the added meta data
    :return: (binary_sequence, ext)
    """

    # Get length from binary sequence
    length_binary = long_binary_sequence[:32]
    length = int(length_binary, 2)

    # Get extension from binary sequence
    binary_list = [long_binary_sequence[32:40], long_binary_sequence[40:48], long_binary_sequence[48:56]]
    char_list = [chr(int(binary, 2)) for binary in binary_list]
    ext = ''.join(char_list)

    return long_binary_sequence[56:56 + length], ext
