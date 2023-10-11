from pdf2image import convert_from_path
from uuid import uuid4

def pdfToImages(filePath):
    images = convert_from_path(filePath)
    image = images[0]
    imageName = f'{uuid4()}.png'
    image.save(f'images/{imageName}', 'PNG')
    return imageName, image.height, image.width