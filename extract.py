import mediapipe as mp
import numpy as np
import cv2
import os
from data_processing import *
from data_collection import *

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

# ====================================================== #
# Settings
height_width =  224 # Supports square outputs for now
output_format = "png" # File format of the image
buffer = 5 # % of padding around the hand
hflipped = True # Flip the video horizontally
vflipped = False # Flip the video vertically
angle = 0 # Angle of rotation
start_extraction = 0 # Number of seconds before starting the extraction
num_sec = 16 # Number of seconds to extract after start_extraction seconds 
# ====================================================== #
# Call process_all() if you want to process all the videos in the input_videos folder
# Call process(filename) if you want to process a specific video in the input_videos folder
# Call process() if you want to use your webcam
# ====================================================== #

folder_path = "input_videos"
video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".wmv")
video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(video_extensions)]

def process(filename = 0):
    folder_name = "camera" if filename == 0 else filename.split(".")[0]
    output_dir = f"output_images/{folder_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    _hand_priority = 'left'
    cap = cv2.VideoCapture(filename) if filename == 0 else cv2.VideoCapture("input_videos/" + filename)
    fps = cap.get(cv2.CAP_PROP_FPS)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.2) as hands:
        frame_count = 0
        frame_passed = 0
        frame_start = fps*start_extraction
        frame_end = frame_start + fps*num_sec
        extracted = False
        while True:
            frame_passed += 1
            ret, frame = cap.read()
            (h, w) = frame.shape[:2]

            frame = cv2.flip(frame,1) if hflipped else frame
            frame = cv2.flip(frame,0) if vflipped else frame
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            frame = cv2.warpAffine(frame, rotation_matrix, (w, h))
            if not ret:
                break
            image, _landmarks_list, _landmark_connections, hand_used = detect_upperbody(frame, hands)
            h, w, _ = image.shape
            if frame_passed >= frame_start and frame_passed <= frame_end:
                extracted = True
                label = f"Extracting for {float((frame_end - frame_passed)/fps):.2f}s"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

                text_x = w - text_size[0] - 10
                text_y = text_size[1] + 10

                cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), (w - 5, text_y + 5), (0, 255, 0), -1)
                cv2.putText(image, label, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

                if _landmarks_list and _landmarks_list.landmark:

                    # Calculate the box
    
                    # buffer = 5
                    xs = [landmark.x for landmark in _landmarks_list.landmark]
                    ys = [landmark.y for landmark in _landmarks_list.landmark]
                    
                    x_min = min(xs) * w 
                    y_min = min(ys) * h
                    x_max = max(xs) * w
                    y_max = max(ys) * h

                    x_len = abs(x_max - x_min)
                    y_len = abs(y_max - y_min)

                    max_len = max([x_len, y_len])
                    padding = (buffer/100)*max_len

                    x_adj = (max_len - x_len)/2 + padding
                    y_adj = (max_len - y_len)/2 + padding

                    x_low = int(x_min - x_adj)
                    x_low = x_low if x_low > 0 else 0
                    x_high = int(x_max + x_adj )
                    x_high = x_high if x_high < w else w
                    y_low = int(y_min - y_adj)
                    y_low = y_low if y_low > 0 else 0
                    y_high = int(y_max + y_adj)
                    y_high = y_high if y_high < h else h

                    x_len = abs(x_max - x_min)
                    y_len = abs(y_max - y_min)
                    
                
                    valid_framing = x_low > 0 and x_high < w and y_low > 0 and y_high < h
                    if valid_framing:
                        if height_width <= int(max_len):
                            interpolation = cv2.INTER_AREA # best for downscaling
                        else:
                            interpolation = cv2.INTER_CUBIC # best for upscaling

                        cv2.rectangle(image, (x_low, y_low), (x_high, y_high), (0, 255, 0), 2)
                        # Text settings
                        label = "Extracted Image"
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 0.5
                        font_thickness = 1
                        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

                        text_x = x_low
                        text_y = y_low - 10 

                        text_y = max(text_size[1], text_y)

                        cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), (text_x + text_size[0], text_y + 5), (0, 255, 0), -1)
                        cv2.putText(image, label, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)


                        cropped_image = cv2.flip(frame,1)[y_low:y_high, x_low:x_high]
                        output_image = cv2.resize(cropped_image, (height_width, height_width), interpolation=interpolation)
                        cv2.imwrite(output_dir + f"\{frame_count}.{output_format}", output_image)
                        frame_count += 1
                    else:
                        cv2.rectangle(image, (x_low, y_low), (x_high, y_high), (0, 0, 255), 2)
                        x_low = x_low if x_low > 0 else 0
                        x_high = x_high if x_high < w else w
                        y_low = y_low if y_low > 0 else 0
                        y_high = y_high if y_high < h else h
                        # Text settings
                        label = "OUT OF FRAME"
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 0.5
                        font_thickness = 1
                        text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

                        text_x = x_low
                        text_y = y_low - 10 

                        text_y = max(text_size[1], text_y)

                        cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), (text_x + text_size[0], text_y + 5), (0, 0, 255), -1)
                        cv2.putText(image, label, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
            else:
                label = f"Extracting in {float((frame_start - frame_passed)/fps):.2f}s" if not extracted else "Done Extraction"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

                text_x = w - text_size[0] - 10
                text_y = text_size[1] + 10

                cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), (w - 5, text_y + 5), (0, 0, 255), -1)
                cv2.putText(image, label, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

            cv2.imshow('Image Extraction', image)

            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def process_all():
    for video in video_files:
        process(video)


# process_all()
process("enye.mp4")



