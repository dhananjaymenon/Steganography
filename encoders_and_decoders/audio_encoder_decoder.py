import wave
import struct
from metadata_functions import use_message_meta
import os
import numpy as np

"""
Helper Function
"""


def convert_to_mono(audio_file):
    """
    As the encoder only works on audio files with a single channel,
    audio files with multiple channels are converted into a mono audio.
    :param audio_file: location of audio_file
    :return: saved mono_audio_file location
    """
    from scipy.io import wavfile
    # Load the stereo .wav file
    sample_rate, stereo_audio = wavfile.read(audio_file)

    # Convert stereo audio to mono by averaging the channels
    mono_audio = np.mean(stereo_audio, axis=1, dtype=np.int16)

    # Save the mono audio to a new .wav file
    wavfile.write(audio_file[:-4] + '_mono.wav', sample_rate, mono_audio)

    return audio_file[:-4] + '_mono.wav'


"""
Audio Encode and Decode
"""


def audio_encode(audio_path: str, binary_message: str, output_path: str):
    input_wav = audio_path
    output_wav = output_path

    # Check if wav_in is mono_audio
    # If wav_in is not mono_audio, it is converted to mono_audio
    obj = wave.open(input_wav, "rb")
    if obj.getnchannels() > 1:
        input_wav = convert_to_mono(input_wav)

    with wave.open(input_wav, 'rb') as wav_in:
        # Create a new WAV file for output
        with wave.open(output_wav, 'wb') as wav_out:

            wav_out.setparams(wav_in.getparams())
            # eg: frames_hex = "b'\x9a\x04M\x04\xf4\x03\x9d\x03O\x03'"
            frames_hex = wav_in.readframes(wav_in.getnframes())

            # eg: frames_int_list = [1178, 1101, 1012, 925, 847, 750, 620, 449, 283, 154]
            frames_int_list = list(struct.unpack(f'{wav_in.getnframes()}h', frames_hex))

            # Converts binary_message_string to list of bits
            bits = [int(bit) for bit in binary_message]

            if len(bits) > len(frames_int_list):
                raise ValueError("Message is too large to be encoded in the audio file")

            for i, bit in enumerate(bits):

                frame = frames_int_list[i]

                if bit == 0:
                    # Set lsb to 0
                    frame &= ~1
                else:
                    # Set lsb to 1
                    frame |= 1

                frames_int_list[i] = frame

            modified_frames = struct.pack(f'{len(frames_int_list)}h', *frames_int_list)
            wav_out.writeframes(modified_frames)

    # Remove temporarily created mono-channel file
    if obj.getnchannels() > 1:
        os.remove(input_wav)

    print(f"message encoded to audio successfully and saved at {output_path}")
    return


def audio_decode(encoded_audio_path: str) -> [str, str]:
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
