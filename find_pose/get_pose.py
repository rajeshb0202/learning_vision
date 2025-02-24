'''
This program estimates the camera pose using a chessboard pattern.
The program opens a webcam and captures the video stream. It then detects the chessboard pattern in the video stream and estimates the camera pose.
The camera pose is estimated using the solvePnP function in OpenCV. The solvePnP function estimates the camera pose using the 3D object points and the 2D image points.
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt

#get the calibration data
data = np.load(r"./calibration_data/camera_calibration_data.npz")
K = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

board_pattern = (7, 7)
board_cellsize = 0.04
board_criteria = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK


obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])


#open a webcam
cap = cv2.VideoCapture(0)
assert cap.isOpened()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    #estimate the camera pose
    success, img_points = cv2.findChessboardCorners(frame, board_pattern, board_criteria)
    
    
    if success:
        # draw chessboard corners
        cv2.drawChessboardCorners(frame, board_pattern, img_points, success)
        ret, rvec, tvec= cv2.solvePnP(obj_points, img_points, K, dist_coeffs)
        
        # print the camera position
        R = cv2.Rodrigues(rvec)[0]
        T = (-R.T @ tvec).flatten()
        info = f'XYZ: [{T[0]:.3f} {T[1]:.3f} {T[2]:.3f}]'
        print(info)
    
    
      
    
    
    cv2.imshow('img', frame)
    k = cv2.waitKey(10)
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
    
    
