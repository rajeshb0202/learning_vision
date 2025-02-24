'''
This program estimates the camera pose using a chessboard pattern.
The program opens a webcam and captures the video stream. It then detects the chessboard pattern in the video stream and estimates the camera pose.
The camera pose is estimated using the solvePnP function in OpenCV. The solvePnP function estimates the camera pose using the 3D object points and the 2D image points.
The program also displays the camera trajectory in a 3D plot using Matplotlib.
Two threads are used in this program: one thread captures the camera pose, and the other thread displays the camera trajectory.
'''

import threading
import numpy as np
import cv2
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' (no GUI), 'Qt5Agg', etc.
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Load camera calibration data
data = np.load("./calibration_data/camera_calibration_data.npz")
K = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

# Chessboard parameters
board_pattern = (7, 7)
board_cellsize = 0.04
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# Open webcam in a separate thread
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Failed to open camera."

# Store trajectory data
T_arr = []

def capture_pose():
    """ Captures frames and computes camera pose in a separate thread. """
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        success, img_points = cv2.findChessboardCorners(frame, board_pattern, None)

        if success:
            cv2.drawChessboardCorners(frame, board_pattern, img_points, success)
            ret, rvec, tvec = cv2.solvePnP(obj_points, img_points, K, dist_coeffs)
            if ret:
                R, _ = cv2.Rodrigues(rvec)
                T = (-R.T @ tvec).flatten()
                T_arr.append(T)
                print(f'XYZ: [{T[0]:.3f} {T[1]:.3f} {T[2]:.3f}]')

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Start OpenCV in a separate thread
threading.Thread(target=capture_pose, daemon=True).start()

# Initialize Matplotlib figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# lines, = ax.plot([], [], [], "ro-", label="Camera Trajectory")
points = ax.scatter([], [], [], "ro-", label="Camera Trajectory")

ax.set_xlim(0, -2)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.set_xlabel('d')
ax.set_ylabel('X Axis')
ax.set_zlabel('Y Axis')

def update(frame_idx):
    """ Updates the 3D trajectory plot with the latest camera positions. """
    if T_arr:
        x_vals, y_vals, z_vals = zip(*T_arr[-30:])
        # x_vals, y_vals, z_vals = T_arr[-1]        //for displaying only the last point
        points._offsets3d = (z_vals, x_vals, y_vals)
        # lines.set_data(x_vals, y_vals)            //for displaying all the points
        # lines.set_3d_properties(z_vals)           //for displaying all the points
    
    plt.pause(0.01)
    # return lines,
    return points,

# Start animation
ani = animation.FuncAnimation(fig, update, interval=100, repeat=False, cache_frame_data=False)

plt.legend()
plt.show()
