from PIL import Image
import numpy as np
import wave
import struct
import re


def add_message_meta(binary_sequence, ext):
    if len(ext) != 3:
        raise Exception("Invalid extension")

    length = len(binary_sequence)

    length_binary = format(length, '032b')
    ext_binary = format(ord(ext[0]), '08b') + format(ord(ext[1]), '08b') + format(ord(ext[2]), '08b')

    return length_binary+ext_binary+binary_sequence


def use_message_meta(binary_sequence):
    # Get length from binary sequence
    length_binary = binary_sequence[:32]
    length = int(length_binary, 2)

    # Get extension from binary sequence
    binary_list = [binary_sequence[32:40], binary_sequence[40:48], binary_sequence[48:56]]
    char_list = [chr(int(binary, 2)) for binary in binary_list]
    ext = ''.join(char_list)

    return binary_sequence[56:56+length], ext


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

        if encoded_text[space_pointer: space_pointer + 2] == "  ":
            binary_message += "1"
            space_pointer += 2

        else:
            binary_message += "0"
            space_pointer += 1

    # Get meta data from the binary sequence
    binary_message, ext = use_message_meta(binary_message)

    return binary_message, ext


"""
Image Encode and Decode
"""


def image_encode(image_path, binary_message, output_path):
    img = Image.open(image_path)

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img = np.asarray(img)
    W, H, _ = img.shape

    # Check if the image is large enough to hold the message
    max_message_length = W * H * 3
    if len(binary_message) > max_message_length:
        raise ValueError('Message is too large to be encoded in the image')

    # Encode the message into the image
    img = img.flatten()
    for idx, bit in enumerate(binary_message):
        val = img[idx]
        val = bin(val)
        val = val[:-1] + bit
        img[idx] = int(val, 2)
    img = img.reshape((W, H, 3))

    encoded_image = Image.fromarray(img)
    encoded_image.save(output_path)

    print("message encoded to image successfully")

    return


def image_decode(encoded_image_path):
    img = np.asarray(Image.open(encoded_image_path))
    img = img.flatten()

    message_binary = "".join([bin(i)[-1] for i in img])

    # Use message length
    message_binary, ext = use_message_meta(message_binary)

    return message_binary, ext


"""
Audio Encode and Decode
"""


def audio_encode(audio_path, binary_message, output_path):
    input_wav = audio_path
    output_wav = output_path

    with wave.open(input_wav, 'rb') as wav_in:
        # Create a new WAV file for output
        with wave.open(output_wav, 'wb') as wav_out:

            wav_out.setparams(wav_in.getparams())

            frames = wav_in.readframes(wav_in.getnframes())

            samples = list(struct.unpack(f'{wav_in.getnframes()}h', frames))

            bits = [int(bit) for bit in binary_message]

            if len(bits) > len(samples):
                raise ValueError("Message is too large to be encoded in the audio file")

            for i, bit in enumerate(bits):

                sample = samples[i]

                if bit == 0:
                    sample &= ~1
                else:
                    sample |= 1

                samples[i] = sample

            modified_frames = struct.pack(f'{len(samples)}h', *samples)

            wav_out.writeframes(modified_frames)

    print("message encoded to audio successfully")

    return


def audio_decode(encoded_audio_path):
    input_wav = encoded_audio_path

    with wave.open(input_wav, 'rb') as wav_in:
        # Read the frames from the input WAV
        frames = wav_in.readframes(wav_in.getnframes())

        # Convert the frames to a list of samples
        samples = list(struct.unpack(f'{wav_in.getnframes()}h', frames))

        # Extract the LSB of each sample to retrieve the binary message
        binary_message = []
        for sample in samples:
            # Get the LSB of the sample
            bit = sample & 1

            # Append the LSB to the binary message
            binary_message.append(str(bit))

        # Convert the binary message to a string
        binary_string = ''.join(binary_message)

        # Use message length
        binary_string, ext = use_message_meta(binary_string)

        return binary_string, ext
