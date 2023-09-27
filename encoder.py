import argparse
from MTB import file_to_binary
from encoders_and_decoders.image_encoder_decoder import image_encode
from encoders_and_decoders.audio_encoder_decoder import audio_encode
from encoders_and_decoders.text_encoder_decoder import text_encode
from encoders_and_decoders.video_encoder_decoder import video_encode
from metadata_functions import add_message_meta

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--secret', help='the media to be hidden', type=str)
parser.add_argument('-c', '--carrier', help='carrier medium', type=str)
parser.add_argument('-o', '--output', help='output file name', type=str)

args = parser.parse_args()


if __name__ == '__main__':
    secret_file_location = args.secret
    secret_ext = secret_file_location[-3:]
    secret_file_location_binary = file_to_binary(secret_file_location)
    secret_file_binary_with_metadata = add_message_meta(secret_file_location_binary, secret_ext)

    carrier = args.carrier
    carrier_ext = carrier[-3:]

    output_path = args.output

    if carrier_ext == 'png':
        image_encode(
            image_path=carrier,
            binary_message=secret_file_binary_with_metadata,
            output_path=output_path
        )
    elif carrier_ext == 'wav':
        audio_encode(
            audio_path=carrier,
            binary_message=secret_file_binary_with_metadata,
            output_path=output_path
        )
    elif carrier_ext == 'txt':
        text_encode(
            text_file_path=carrier,
            binary_message=secret_file_binary_with_metadata,
            output_path=output_path
        )
    elif carrier_ext == 'mov':
        video_encode(
            video_path=carrier,
            binary_message=secret_file_binary_with_metadata,
            output_path=output_path
        )
    else:
        raise Exception(f"Invalid carrier {carrier_ext}: Valid extensions - 'txt', 'png', 'wav', 'mov'")