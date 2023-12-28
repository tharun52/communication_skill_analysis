#installing and setting up dependencies
import cv2
from keras.models import load_model
from keras.utils import img_to_array
from keras.preprocessing import image
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import os
from time import sleep

    
#opencv's cascadeclassifier file
face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml') #change the path accordingly before executing #absolute path/full path
#loading the pre-trained model (or custom trained one) 
classifier =load_model(r'model.h5')  #change the path accordingly before executing #absolute path/full path

#list of emotions(note: only these 7 were used on the model)
emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

#mediapipe's tools
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

#metrics for evaluation
stage = None
con_cnt= 0 #confidnece count per frame
sl_cnt = 0 #slouched count per frame
p_cnt = 0 #positive emotion count per frame
n_cnt = 0 #negative emotion count per frame

#function for calculating angle between landmarks - refer angle.ipynb in notebooks_tests folder
def calculate_angle(a,b,c):
    a = np.array(a) #start
    b = np.array(b) #mid
    c = np.array(c) #end
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
    return angle

#function for calculating distance between landmarks for pose estimation
def calculate_dist(d1, d2):
    x1, y1 = d1
    x2, y2 = d2
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def analyze_video(path):
    #video capture - default would be 0 i.e integrated webcam, else increase number for different attached devices like 1,2,3... 
    # for custom videos input the path cv2.VideoCapture('Path goes here') instead of device's number
    cap = cv2.VideoCapture(path)

    #setup mediapipe instance & reading the video
    with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
            #recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            #make detection
            results = pose.process(image)
            
            #recolor back to BGR       
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            #set up labels
            labels = []
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            #detecting and showing emotion label around the face
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)


                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = classifier.predict(roi)[0]
                    label=emotion_labels[prediction.argmax()]
                    print(label)
                    if label in ['Happy', 'Neutral']:
                        p_cnt += 1
                    else:
                        n_cnt += 1
                    label_position = (x,y)
                    cv2.putText(image,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                else:
                    cv2.putText(image,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            #extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                #get coordinates
                h_l = [landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y]
                h_r = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]
                s_l = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
                s_r = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]

                #distance b/w nose n shoulder
                m_l = [landmarks[mp_holistic.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_holistic.PoseLandmark.MOUTH_LEFT.value].y]
                m_r = [landmarks[mp_holistic.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[mp_holistic.PoseLandmark.MOUTH_RIGHT.value].y]

                dist1 = calculate_dist(m_l, s_l)
                print(dist1)
                dist2 = calculate_dist(m_r, s_r)
                
                #calculate angle
                angle_1 = calculate_angle(h_l, s_l, s_r)
                angle_2 = calculate_angle(h_r, s_r, s_l)
                
                avg_angle = (angle_1+angle_2) / 2
                print(avg_angle)
                #posture detection logic - warning the values differ for each person hence it's not one fit all solution 
                #could proceed with custom calibration or train a new model with desired metrics based on customer's demands
                if (avg_angle >= 75 and avg_angle <= 90) and (dist1 >= 0.25 and dist1 <=0.40) and (dist2 >= 0.25 and dist2 <=0.40):
                    con_cnt += 1
                    stage = "Confident"
                else:
                    sl_cnt += 1
                    stage = "slouched"
                    
                # Setup status box
                cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
                
                # Stage data
                cv2.putText(image, 'STAGE', (65,12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, 
                (60,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
    
                #visualize
                cv2.putText(image, str(round(avg_angle,2)),
                            tuple(np.multiply(s_l, [640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(round(dist1,2)),
                            tuple(np.multiply(m_l, [640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, str(round(dist2,2)),
                tuple(np.multiply(m_r, [640,480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
            except:
                pass
            
            #render detections
            
            #face landmarks
            
            #optional facemesh - could use this to detect emotions when coupled with some complex math functions instead of training a model
            
            # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
            #                           mp_drawing.DrawingSpec(color=(245,110,60), thickness=2, circle_radius=1))
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
            
            cv2.imshow("mediapipe instance feed", image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()

    #calculating the metrics based on their individual instance on each frame0
    confident_level = con_cnt / (con_cnt + sl_cnt)
    emotional_level = p_cnt / (p_cnt + n_cnt)

    return confident_level, emotion_labels


confident_level , emotional_level = analyze_video(r'dataset/video1.mp4')
#converting it into percentage format and displaying result
print("Confidence level: {:.2%}".format(confident_level))
print("Emotional level: {:.2%}".format(emotional_level))

#rounding up the values and returning it
confident_level = round(confident_level,2)
emotional_level = round(emotional_level, 2)
print(confident_level, emotional_level)
