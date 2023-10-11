from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from os import makedirs, remove
from uuid import uuid4
import math

from analyzer import detectFooter
from utils import pdfToImages

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static_files(filename):
    return send_from_directory('static', filename)


@app.route('/api/upload', methods=['POST'])
def upload():
    fileName = None
    footer_y_position = -1

    try:
        file = request.files['file']
        fileName = f'{uuid4()}.pdf'
        file.save(f'uploads/{fileName}')
    except Exception as e:
        print(e)

    if fileName is not None:
        imagePath, height, width = pdfToImages(f'uploads/{fileName}')
        footer_y_position = math.trunc(detectFooter(f'images/{imagePath}'))
        remove(f'uploads/{fileName}')
        remove(f'images/{imagePath}')

    if (footer_y_position == -1 or footer_y_position < (height/2)):
        response = {'status': 'error', 'data': 'No footer detected'}
        return jsonify(response), 400
    else:
        response = {'status': 'success', 'data': {
            'y': footer_y_position, 'height': height, 'width': width}}
        return jsonify(response), 201


if __name__ == '__main__':
    makedirs('images', exist_ok=True)
    makedirs('uploads', exist_ok=True)
    app.run(port=3000, host='0.0.0.0')
