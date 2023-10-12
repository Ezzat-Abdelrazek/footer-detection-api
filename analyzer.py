import layoutparser as lp
import cv2
import uuid


def size_key(element):
    width = element.width
    height = element.height
    size = width * height
    return size


def detectFooter(imagePath: str):
    """
    @param imagePath: path to the image to be analyzed
    @return: y position of the footer upper boundary
    """
    model = lp.models.Detectron2LayoutModel(
        "lp://TableBank/faster_rcnn_R_50_FPN_3x/config",
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.9],
        label_map={
            1: "TextRegion",
            2: "ImageRegion",
            3: "TableRegion",
            4: "MathsRegion",
            5: "SeparatorRegion",
            6: "OtherRegion",
        },
    )
    image = cv2.imread(imagePath)
    image = image[..., ::-1]
    layout = model.detect(image)
    return analyzeLayout(layout, image)


def analyzeLayout(layout, image) -> int:
    """
    @param layout: layout object generated by the model
    @return: y position of the footer upper boundary
    """
    imageHeight = image.shape[0]

    bottomInterval = lp.Interval(imageHeight * 0.7, imageHeight, axis="y")
    layout = layout.filter_by(bottomInterval)
    layout = layout.sort(key=size_key)

    if layout.__len__() == 0:
        return -1
    bottomBlock_y = layout[-1].block.y_1
    return bottomBlock_y
