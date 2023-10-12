import layoutparser as lp
import cv2
import numpy as np


def size_key(element):
    width = element.width
    height = element.height
    size = width * height
    return size


def detectLines(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
    )

    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 10:
            horizontal_lines.append(line)

    return horizontal_lines


def detectFooter(imagePath: str):
    """
    @param imagePath: path to the image to be analyzed
    @return: y position of the footer upper boundary
    """

    model = lp.Detectron2LayoutModel(
        "lp://PrimaLayout/mask_rcnn_R_50_FPN_3x/config",
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.6],
        label_map={
            1: "TextRegion",
            2: "ImageRegion",
            3: "TableRegion",
            4: "MathsRegion",
            5: "SeparatorRegion",
            6: "OtherRegion",
            7: "Row",
        },
    )

    image = cv2.imread(imagePath)
    image = image[..., ::-1]
    layout = model.detect(image)

    return analyzeLayout(layout, image)


def analyzeLayout(layout, image):
    """
    @param layout: layout object generated by the model
    @return: y position of the footer upper boundary
    """

    imageHeight = image.shape[0]
    bottomInterval = lp.Interval(imageHeight * 1, imageHeight, axis="y")
    layout = layout.filter_by(bottomInterval)
    layout = layout.sort(key=size_key)

    if layout.__len__() == 0:
        return -1

    horizontal_lines = detectLines(image)

    # Use horizontal lines

    bottomBlock_y = layout[-1].block.y_1
    return bottomBlock_y
