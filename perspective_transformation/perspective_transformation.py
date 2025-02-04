import os 
import cv2 as cv 
import numpy as np 
import matplotlib.pyplot as plt 

def perspectiveTransform(): 
   # Define image path
    imgPath = os.path.join(r'./images/building_v1.jpg')

    # Load and convert image to RGB format
    img = cv.imread(imgPath)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Get image dimensions
    height, width = img.shape[:2]

    # Define the original four corner points in the source image
    p1 = np.array([[0, 0],
                [width - 1, 0],
                [0, height - 1],
                [width - 1, height - 1]], dtype=np.float32)


    # Define another set of transformation points for perspective
    n = 300  # Offset value
    p2 = np.array([[n, n],  # Move top-left corner inward
                    [width - n, n],  # Move top-right corner inward
                    [0, height],  # Keep bottom-left
                    [width, height]], dtype=np.float32)  # Keep bottom-right


    # Define another set of transformation points for perspective. This time with scaling
    # Scale transformation matrix
    scale_factor = 0.5
    p3 = p2 * scale_factor  # Element-wise scaling of transformation points

    # Compute the perspective transformation matrix
    T = cv.getPerspectiveTransform(p1, p3)

    # Check the rank of the transformation matrix
    rank_t = np.linalg.matrix_rank(T)
    print("Rank of T:", rank_t)

    # Apply perspective transformation
    imgTrans = cv.warpPerspective(img, T, (int(width * scale_factor), int(height * scale_factor)))

    # Display the original and transformed images
    cv.imshow("Original", img)
    cv.imshow("Perspective", imgTrans)
    cv.waitKey(0)
    cv.destroyAllWindows()

    

if __name__ == '__main__': 
    perspectiveTransform()