from flask import Flask, render_template, request, jsonify
import cv2
import os
from deepface import DeepFace
import base64
import numpy as np

app = Flask(__name__)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Could not open webcam device")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)


reference_dir = "C://Users//ajayu//Documents//Programming//Python//ML//Faceauth//"
reference_images = [os.path.join(reference_dir, filename) for filename in os.listdir(reference_dir) if filename.endswith('.jpg')]

@app.route('/')
def index():
    return render_template('index.html')

def checkface(frame, image_paths):
    for image_path in image_paths:
        try:
            reference_image = cv2.imread(image_path)
            result = DeepFace.verify(frame, reference_image, enforce_detection=False)['verified']
            if result:
                print(f"Match found with reference image: {image_path}")
                return True 
        except Exception as e:
            print(f"Error during face verification with {image_path}: {e}")
    return False 

@app.route('/detect', methods=['POST'])
def detect():
    try:
        
        image_data = request.form['image_data'].split(',')[1]  
        decoded_image = base64.b64decode(image_data)
        
        
        if len(decoded_image) == 0:
            return jsonify({'error': 'Empty image data'})

        np_image = np.frombuffer(decoded_image, dtype=np.uint8)
        
        if np_image.size == 0:
            return jsonify({'error': 'Invalid image data'})


        frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        match_found = checkface(frame, reference_images)

        if match_found:
            return jsonify({'match_found': True})
        else:
            return jsonify({'match_found': False})

    except Exception as e:
        print('Error during face detection:', e)
        return jsonify({'error': 'Face detection error'})

@app.route('/login_success')
def login_success():
    return render_template('login_success.html')
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0')