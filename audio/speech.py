from transformers import pipeline

def recognize_speech(paths):
    text = ''
    # print(paths)
    # print(type(paths))
    for path in paths:
        # print(type(path))
        # print(path)
        text = text + recognize_speech_individual(path)+" "
    return text.lower()
def recognize_speech_individual(audio_file_path):
    # Load the Hugging Face ASR pipeline
    asr_pipeline = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

    # Load the audio file
    with open(audio_file_path, "rb") as audio_file:
        # Perform speech recognition
        result = asr_pipeline(audio_file.read())

    # Extract the recognized text from the result
    recognized_text = result['text']

    return recognized_text
if __name__ == "__main__":
    wav_file_paths = ['cache/video1_audio_part1.wav', 'cache/video1_audio_part2.wav', 'cache/video1_audio_part3.wav', 'cache/video1_audio_part4.wav']
    print(recognize_speech(wav_file_paths))