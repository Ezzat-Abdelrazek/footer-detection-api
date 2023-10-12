import cv2
import numpy as np


def detectFooter(imagePath: str):
    """
    @param imagePath: path to the image to be analyzed
    @return: y position of the footer upper boundary
    """
    # Load the image
    image = cv2.imread(imagePath)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
    )

    # Find the line with the highest y position
    max_y = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        max_y = max(max_y, y1, y2)

    return max_y
