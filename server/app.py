import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the pre-trained model
model = load_model('pdmodel.h5')

# Define a function to process the uploaded image and make predictions
def predict_image(file_path):
    img = image.load_img(file_path, target_size=(64, 64))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255.0  # Normalize the image
    result = model.predict(img)
    return result[0]

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        result = predict_image(file_path)
        # os.remove(file_path)  
        if result[0]<0:
            return jsonify({'result':"The image classified is Healthy", 'image_url': file_path})
        else:
            return jsonify({'result': "Parkinson's disease detected", 'image_url': file_path})


if __name__ == '__main__':
    app.run(debug=True)
