import argparse
import os.path
import errno

from MTB import *
from lsb import *

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--encoded', help='encoded file location', type=str)
parser.add_argument('-d', '--decoded', help='location to save decoded file', type=str)

args = parser.parse_args()


if __name__ == '__main__':
    encoded = args.encoded
    output_path = args.decoded

    # Check if paths exists
    if not os.path.exists(encoded):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), encoded)

    if not os.path.exists(output_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), output_path)

    if output_path.endswith("/"):
        output_path = output_path[:-1]

    # Check encoded type
    encoded_ext = encoded[-3:]
    if encoded_ext == 'png':
        binary_decoded, ext = image_decode(
            encoded_image_path=encoded
        )
    elif encoded_ext == 'wav':
        binary_decoded, ext = audio_decode(
            encoded_audio_path=encoded
        )
    elif encoded_ext == 'txt':
        binary_decoded, ext = text_decode(
            encoded_text_path=encoded
        )
    else:
        raise Exception("extension of encoded file location not supported")

    file_name = os.path.basename(encoded[:-4])
    binary_to_file(binary_string=binary_decoded, output_file=f"{output_path}/{file_name}_decoded", ext=ext)
    print(f"message decoded and saved at {output_path}/{encoded_ext}_decoded.{ext}")