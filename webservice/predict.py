import os
#import pickle
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
from tensorflow import keras

#with open('model.bin', 'rb') as f_out:
   # model = pickle.load(f_out)
model = keras.models.load_model('HARmodel_main.h5')
labels = {
    0: "sitting",
    1: "using laptop",
    2: "hugging",
    3: "sleeping",
    4: "drinking",
    5: "clapping",
    6: "dancing",
    7: "cycling",
    8: "calling",
    9: "laughing",
    10: "eating",
    11: "fighting",
    12: "listening_to_music",
    13: "running",
    14: "texting"
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
