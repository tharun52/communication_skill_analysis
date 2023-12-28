# Softskill Communication Analysis

## Overview

This repository presents a comprehensive solution for soft skill communication analysis, offering insights into both posture and emotional confidence levels through the meticulous analysis of video frames. The system leverages various Python libraries and tools, and all dependencies can be installed by using the REQUIREMENTS.txt file.

## Installation

To run the code start by installing the required dependencies using the following command:

pip install -r requirements.txt


## Project Configuration

1. **Model File (model.h5):**
   Confirm the presence of the model.h5 file, representing the trained machine learning model for emotion recognition. The model has an accuracy rate of 60% but it not super custom trained hence it is not ideal for the task.

2. *Haarcascade File:*
   Integrate the Haarcascade file within the project structure. This file is crucial for efficient face detection during video analysis.

3. *Path Configuration:*
   Customize file paths in the code to align with your project structure. This step ensures smooth execution and accurate referencing of model and Haarcascade files.

4. *Video Source Modification:*
   Tailor the video source by adjusting the following line in the code:
   python
   cv2.VideoCapture(0)
   
   Replace 0 with the path to the desired pre-recorded video for analysis.

## Performance Considerations

- *Frame-by-Frame Analysis:*
   The analysis operates frame by frame using OpenCV, providing detailed insights into posture and emotional states. Note that processing pre-recorded videos may exhibit a slightly slower performance due to the nature of frame-based analysis. Refer to code comments for an in-depth understanding of the implementation.

- *Visual Analysis Components:*
   - *Posture Confidence Level:*
      Utilizing Mediapipe joint landmarks, the system assesses posture confidence, offering valuable insights into body language and gestures.
   - *Emotional Confidence Level:*
      Leveraging the custom-trained model 'model.h5,' the analysis extends to emotional states, providing an additional layer of understanding during communication.

## Output

Upon completing the frame-by-frame analysis, the system outputs two critical variables:

1. *Posture Confidence:*
   A measure of confidence in the observed posture and body language.

2. *Emotional Confidence:*
   Reflecting the model's confidence in predicting emotional states.

## Model Training

The model's training involved utilizing the extensive [Face Expression Recognition Dataset](https://www.kaggle.com/datasets/jonathanoheix/face-expression-recognition-dataset).

## Testing and Reliability

This implementation serves primarily as a testing solution and is not recommended for production use. The accuracy of the analysis is substantial but may require further refinement for specific use cases.

## Contributing

Contributions to this project are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## Acknowledgments

Special thanks to the following for inspiration, guidance and resources that played a crucial role in the development of this soft skill communication analysis project:

- [Mediapipe](https://google.github.io/mediapipe/): For providing a powerful library for hand and pose estimation, essential for posture confidence analysis.

- [Emotion_Detection_CNN](https://github.com/akmadan/Emotion_Detection_CNN): A valuable resource for inspiration and insights into emotion detection using convolutional neural networks.

- [Nicholas Renotte's YouTube Tutorial](https://youtu.be/Bb4Wvl57LIk?si=zMjlSYHZpxKDw8pc): For providing educational content on utilizing deep learning for emotion recognition.

- [YouTube Tutorial on Face Expression Recognition](https://www.youtube.com/watch?v=pG4sUNDOZFg&ab_channel=NicholasRenotte): A helpful tutorial for understanding the fundamentals of face expression recognition.

Feel free to explore the notebooks_tests folder for an in-depth understanding, as various components were tested and implemented separately in the notebooks.


Special thanks to the contributors of the [Face Expression Recognition Dataset](https://www.kaggle.com/datasets/jonathanoheix/face-expression-recognition-dataset) for their invaluable dataset.
