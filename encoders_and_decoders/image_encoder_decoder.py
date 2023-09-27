from PIL import Image
import numpy as np
from metadata_functions import use_message_meta

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

    if image_path != output_path:
        print(f"message encoded to image successfully and saved at {output_path}")

    return


def image_decode(encoded_image_path):
    img = np.asarray(Image.open(encoded_image_path))
    img = img.flatten()

    message_binary = "".join([bin(i)[-1] for i in img])

    # Use message length
    message_binary, ext = use_message_meta(message_binary)

    return message_binary, ext