# ========================================================
# Image Capture from Webcam with Pause/Continue and Quit
# ========================================================
#
# This script captures images from the webcam at regular intervals.
# 
# Instructions:
# - Press 'q' to quit the task immediately.
# - Press 'p' to pause the capture; press 'p' again to continue.
#
# The captured images are saved in the specified directory.
# ========================================================


import cv2
import numpy as np
import os
import time
import string
import shutil

def save_frame(frame, path, clicked_images_count):
    file_name = f"{clicked_images_count}.jpg"
    file_path = os.path.join(path, file_name)
    cv2.imwrite(file_path, frame)
    
    


def init_directory(img_folder_path, dir_name):
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
        print(f"Created the directory: {dir_name} inside {img_folder_path} ")
    else:
        print(f"the directory {dir_name} already exists: {img_folder_path} ")
    return
  
    
    
    

def take_images_regular_interval(interval, num_images, dir_name="default", source_webcam = 0):
    """
    Capture images from the webcam at regular time intervals.
    """
    
    img_folder_path = os.path.join(os.getcwd(), "images", dir_name)
    init_directory(img_folder_path, dir_name)
        
    
    clicked_images_count = 0
    time_counter = 0
    last_measured_time =  time.time()
    
    print("starting webcam to click photos")
    cap = cv2.VideoCapture(source_webcam)
    
    while clicked_images_count < num_images:
        # read the frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        # if the frame read is successull, then proceed
        if ret:
            live_frame = frame.copy()                   #copy the frame into a live_frame
            
            # implmented a time_counter between each clicks
            if time.time() - last_measured_time > 1.0:
                time_counter += 1
                if time_counter > interval:
                    # save the current frame
                    clicked_images_count += 1
                    save_frame(frame= frame, path= img_folder_path, clicked_images_count = clicked_images_count)
                    cv2.putText(frame, str(clicked_images_count), (int(width // 2), int(height // 2)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,255,0), 5)
                    cv2.imshow("saved_frame", frame)
                    print("Number of photos_clicked: ", clicked_images_count)
                    time_counter = 0
                    
                                
                last_measured_time = time.time()
            
            
            # dispaly the live_frame with the time counter
            height, width = frame.shape[:2]
            cv2.putText(live_frame, str(time_counter), (int(width // 2), int(height // 2)), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,0), 5)
            cv2.imshow("display_frame", live_frame)
            
            
            
            key = cv2.waitKey(1) 
            # if user presses 'q' then it quits in the middle
            if key == ord('q') :
                print("Task stopped in the middle... closing down")
                cap.release()
                break
            # if user presses 'p' then it will pause/continue
            if key == ord('p'):
                while True:
                    key = cv2.waitKey(1)
                    if key == ord('p'):
                        break
        

    return clicked_images_count



# ================================
# Main Execution
# ================================
    
    
num_images = 30             # number of images to be clicked
interval = 6                # interval in seconds
dir_name='logitech_2'       # directory name in which the clicke dimages is to be stored
source_webcam = 0


clicked_count = take_images_regular_interval(interval = interval, num_images=num_images, dir_name=dir_name, source_webcam= source_webcam)
cv2.destroyAllWindows()
if clicked_count == num_images:
    print(f"Task completed. Clicked {clicked_count} images...")
else:
    print(f"Task stopped in the middle. Clicked {clicked_count} images....")
    

    