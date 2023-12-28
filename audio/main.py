# importing functions from other files
from speech import recognize_speech
from tk import show_triple_section_dialog
from accuracy_score import calculate_grammar_accuracy
from video_to_wav import extract_audio_from_video
from delete_file import delete_file
from correct_text1 import correct_grammar
import sys

# Get the video file path from the user
path = input("Enter the video file path : ")

# Check if the file has a '.mp4' extension
if path[-4:].lower() != '.mp4':
    sys.exit("non mp4 error")
else:
    # Extract audio from the video
    output_audio_paths = extract_audio_from_video(path)

    # Transcribe the audio
    transcribed_text = recognize_speech(output_audio_paths)

    # Correct the grammar in the transcribed text
    correct_text = correct_grammar(transcribed_text)

    # Calculate grammar accuracy
    score = calculate_grammar_accuracy(transcribed_text, correct_text)

    # Delete the temporary audio file
    delete_file(output_audio_paths)

    # Display the triple-section dialog
    show_triple_section_dialog(transcribed_text, correct_text, score)
