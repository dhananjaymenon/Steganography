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


def audio_encode(audio_path, binary_message, output_path):
    input_wav = audio_path
    output_wav = output_path

    # Check if wav_in is mono_audio
    obj = wave.open(input_wav, "rb")
    if obj.getnchannels() > 1:
        input_wav = convert_to_mono(input_wav)

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

    # Remove temporarily created mono-channel file
    if obj.getnchannels() > 1:
        os.remove(input_wav)

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
