import os
import moviepy.editor as mp

def extract_audio_from_video(video_path, cache_folder="cache", max_duration=120):
    """
    Extract audio from a video file and save it as WAV files in smaller parts if the video duration is more than max_duration.

    Parameters:
    - video_path (str): Path to the input video file.
    - cache_folder (str): Folder to save the extracted audio. Default is "cache".
    - max_duration (int): Maximum duration of each audio segment in seconds. Default is 60 seconds.
    """
    paths = []
    # Create the cache folder if it doesn't exist
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    # Load the video
    video = mp.VideoFileClip(video_path)

    # Get the total duration of the video
    total_duration = video.duration

    # Calculate the number of segments needed
    num_segments = int(total_duration / max_duration) + 1

    for i in range(num_segments):
        # Calculate the start and end times for each segment
        start_time = i * max_duration
        end_time = min((i + 1) * max_duration, total_duration)

        # Extract the audio from the video for the current segment
        audio_segment = video.subclip(start_time, end_time).audio

        # Formulate the output audio file path in the cache folder
        output_audio_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_audio_part{i + 1}.wav"
        output_audio_path = os.path.join(cache_folder, output_audio_filename)
        
        # Write the audio to a WAV file
        audio_segment.write_audiofile(output_audio_path, codec='pcm_s16le', ffmpeg_params=["-ac", "2"])

        paths.append(output_audio_path.replace('\\', '/'))

    # Close the video file clip
    video.close()

    return paths

if __name__ == "__main__":
    # Replace 'input_video.mp4' with your video file
    video_path = 'data/video1.mp4'

    # Extract audio from the video and save it in the cache folder
    print(extract_audio_from_video(video_path))
