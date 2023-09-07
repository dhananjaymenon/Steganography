import shutil
import cv2
import os
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image

from image_encoder_decoder import image_encode
from metadata_functions import add_frame_meta, use_message_meta

"""
Helper Functions
"""


def get_frame_max(original_video_path):
    """
    Returns the maximum length of binary string that can be stored in
    a frame
    """
    # Get dimension of video
    vcap = cv2.VideoCapture(original_video_path)

    if vcap.isOpened():
        width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frame_max = width * height * 3
    else:
        raise Exception("Video path is incorrect")

    return frame_max


def video_to_frames(video_path, output_dir):
    """
    Converts a video to a directory of frames
    """
    # Create the output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize a frame counter
    frame_count = 0

    # Read frames from the video
    while True:
        ret, frame = cap.read()

        # Break the loop if no frames are left
        if not ret:
            break

        # Define the output frame path
        frame_path = os.path.join(output_dir, f'frame_{frame_count:04d}.png')

        # Save the frame as PNG
        cv2.imwrite(frame_path, frame)

        # Increment frame counter
        frame_count += 1

        # Display progress
        print(f"Saved frame {frame_count}")

    # Release the video capture
    cap.release()

    print("Frame extraction complete!")


def frames_to_video(frames_dir, original_video_path, output_video_path):
    """
    Converts a directory of frames to a video.
    """
    output_video_without_sound_path = 'output_video_without_sound.mov'

    # Get frame dimensions from the original video
    cap_original = cv2.VideoCapture(original_video_path)
    frame_width = int(cap_original.get(3))
    frame_height = int(cap_original.get(4))
    frame_fps = int(cap_original.get(5))

    # Define the codec and create VideoWriter object
    # Note: FFV1 is used to prevent compression of frames when making the video
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # You can change the codec if needed
    out = cv2.VideoWriter(output_video_without_sound_path, fourcc, frame_fps, (frame_width, frame_height), isColor=True)

    # Loop through frames in the directory and add them to the output video
    frame_count = 0
    while True:
        frame_path = os.path.join(frames_dir, f'frame_{frame_count:04d}.png')
        if not os.path.exists(frame_path):
            break

        frame = cv2.imread(frame_path)
        out.write(frame)

        print(f"Added frame {frame_count} to the output video")
        frame_count += 1

    # Release the output VideoWriter
    out.release()

    # Path to the generated video (from the previous script)
    generated_video_path = output_video_without_sound_path

    # Load the generated video
    generated_clip = VideoFileClip(generated_video_path)

    # Load the original video to extract audio
    original_clip = VideoFileClip(original_video_path)
    audio = original_clip.audio

    # Combine the generated video with the original audio
    final_clip = generated_clip.set_audio(audio)

    # Write the final video with sound
    final_clip.write_videofile(output_video_path, codec='rawvideo', audio_codec='aac')

    # Delete created temporary files
    os.remove(output_video_without_sound_path)

    print("Video with sound generation complete!")


"""
Video Encode and Decode
"""

def video_encode(video_path, binary_message, output_path):

    # Convert video to a list of frames
    frame_dir = "temp_encode"
    video_to_frames(video_path, frame_dir)

    # Get frame max
    frame_max = get_frame_max(video_path)

    # add frame_meta
    binary_message = add_frame_meta(binary_message, frame_max)
    print(binary_message)

    # Number of frames required
    number_of_frames_binary = binary_message[:32]
    number_of_frames = int(number_of_frames_binary, 2)
    print(number_of_frames_binary, number_of_frames)

    # Get list of image names from directory
    images = [os.path.join(frame_dir, filename) for filename in os.listdir(frame_dir)]

    # add message to images
    binary_segments = [binary_message[i:i+frame_max] for i in range(number_of_frames)]
    print(binary_segments)

    image_index = 0
    for binary_segment in binary_segments:
        image = images[image_index]
        image_encode(image, binary_segment, image)
        print(image, image_index, binary_segment)

    # Convert directory of images to a video
    frames_to_video(frame_dir, video_path, output_path)


def video_decode(encoded_video_path):
    # Convert video to a list of frames
    frame_dir = "temp_decode"
    video_to_frames(encoded_video_path, frame_dir)

    # Get list of image names from directory
    images = [os.path.join(frame_dir, filename) for filename in os.listdir(frame_dir)]
    first_frame = images[0]

    # Get number of frames
    img = np.asarray(Image.open(first_frame))
    img = img.flatten()
    binary_sequence_first_frame = "".join([bin(i)[-1] for i in img])
    number_of_frames_binary = binary_sequence_first_frame[:32]
    number_of_frames = int(number_of_frames_binary, 2)
    print(number_of_frames_binary, number_of_frames)

    # Get binary sequence
    message_binary = ""
    print(number_of_frames)
    for i in range(number_of_frames):
        encoded_image_path = images[i]
        print(encoded_image_path)
        img = np.asarray(Image.open(encoded_image_path))
        img = img.flatten()

        message_binary += "".join([bin(i)[-1] for i in img])
        print(i)

    print(message_binary[:32])
    # Use meta data
    message_binary, ext = use_message_meta(message_binary[32:])
    print(message_binary)
    print(ext)

    return message_binary, ext
