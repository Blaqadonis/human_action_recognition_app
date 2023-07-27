import os
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras


model = tf.keras.models.load_model("HARmodel_main.h5")


labels = {
    0: "calling",
    1: "clapping",
    2: "cycling",
    3: "dancing",
    4: "drinking",
    5: "eating",
    6: "fighting",
    7: "hugging",
    8: "laughing",
    9: "listening_to_music",
    10: "running",
    11: "sitting",
    12: "sleeping",
    13: "texting",
    14: "using_laptop"
}

def preprocess_image(image):
    '''Preprocessing'''
    image = image.resize((160, 160))
    image = np.array(image)
    image = image / 255.0
    return image

def predict(image):
    '''Predicting'''
    preprocessed_image = preprocess_image(image)
    preds = model.predict(np.asarray([preprocessed_image]))
    return preds[0]

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    '''App service'''
    if 'image' in request.files:
        file = request.files['image']
        image = Image.open(file)
        pred = predict(image)
        label_index = np.argmax(pred)
        label = labels[label_index]
        return jsonify({'prediction': label})
    else:
        return jsonify({'error': 'No image file found in the request.'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
