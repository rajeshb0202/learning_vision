import numpy as np
import cv2
import glob
import os

# Chessboard size (number of inside corners per row and column)
chessboard_size = (7,7)  # Adjust according to your chessboard
square_size = 25  # Size of each square in mm (change as needed)

# Termination criteria for refining corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points (3D points in real-world space)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3D world points
imgpoints = []  # 2D image points

# Load chessboard images
folder_name = "logitech_1"
imgs_path = os.path.join("images", folder_name, "*.jpg")
image_files = glob.glob(imgs_path)  # Update path if needed

print(len(image_files))

for fname in image_files:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)

        # Refine the corner locations
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('Detected Corners', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# Perform camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


# Print results
print("Camera matrix:\n", camera_matrix)
print("\nDistortion coefficients:\n", dist_coeffs)

# Save calibration data
calibration_fname = os.path.join("calibration_data", f"{folder_name}.npz")
np.savez(calibration_fname, camera_matrix=camera_matrix, dist_coeffs=dist_coeffs, rvecs=rvecs, tvecs=tvecs)
print("saved the calibration data in the: ", calibration_fname)


# # Test undistortion on a sample image
# test_img = cv2.imread(image_files[0])
# h, w = test_img.shape[:2]
# new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

# # Undistort
# undistorted_img = cv2.undistort(test_img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# # Show results
# cv2.imshow('Original Image', test_img)
# cv2.imshow('Undistorted Image', undistorted_img)
# cv2.waitKey(0)
# cv2.destroyAll
