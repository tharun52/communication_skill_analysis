# Project Overview

## Installation

### Run the following command to install the required packages:

pip install -r requirements.txt

### To run the program, execute the following command:

python main.py

# Explanation of Files

1. **main.py**: This file serves as the central orchestrator, calling functions from each module to facilitate the overall execution of the program.

2. **video_to_wav.py**: This module accepts a video file path as input and efficiently converts it into multiple WAV files. Each resulting WAV file is carefully crafted to be no longer than 2 minutes. The conversion process is implemented using the MoviePy library, ensuring seamless handling of video-to-audio transformations.

3. **speech.py**: Designed for handling multiple audio files as input, this module transcribes the contained text by leveraging audio recognition techniques. The output is a concatenated text from all the audio files. It's important to note that the recognition model utilized here is the Hugging Face pipeline model. Due to its slow and memory-intensive nature, the video is preprocessed by splitting it into multiple WAV files. Alternatively, you have the option to use the Google Speech Recognition model, which, although less accurate, requires an internet connection.

4. **correct_text1.py**: This module is dedicated to text correction. It employs an OpenAI model for this purpose, necessitating an API key for proper functioning. Users should replace the placeholder 'api-key' with their actual OpenAI API key to ensure the correct operation of the text correction functionality.

5. **correct_text.py**: An alternative text correction model is provided in this module. Unlike its counterpart above, it does not require an API key for access. However, it's essential to be aware that this alternative model is less accurate. To use this model, replace 'from correct_text1 import correct_grammar' with 'from correct_text import correct_grammar' in line 7 of the main.py file.

6. **accuracy_score.py**: This module focuses on generating an accuracy score by comparing the transcribed text with the corrected text. The comparison process utilizes the difflib library, allowing for a quantitative assessment of the transcription accuracy.

7. **delete_file.py**: In this module, files are deleted based on a provided list of paths. It offers a convenient way to manage and clean up unwanted files.

8. **tk.py**: This module is responsible for displaying a Tkinter dialog box for program output. Tkinter is a widely used Python library for creating graphical user interfaces, and its implementation in this module enhances the user experience by providing an interactive output display.

