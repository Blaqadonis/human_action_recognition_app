import numpy as np

from tensorflow import keras
from PIL import Image

from flask import Flask, request, jsonify
import mlflow
import mlflow.tensorflow



mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment('Blaqs_har_classifier')


# Load the trained model
model = keras.models.load_model('HARmodel_main.h5')

# Define the labels
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

# Process the image
def preprocess_image(image):
    '''Preprocessing '''
    image = image.resize((160, 160))
    image = np.array(image)
    image = image / 255.0
    return image

# Make predictions
def predict(image):
    '''Predicting image '''
    preprocessed_image = preprocess_image(image)
    preds = model.predict(np.asarray([preprocessed_image]))
    return preds[0]

# Flask app
app = Flask('Blaqs_Human_Action_Recognition_App')

@app.route('/tracking_predict', methods=['POST'])
def predict_endpoint():
    '''Prediction service '''
    with mlflow.start_run():
        mlflow.tensorflow.autolog()
        mlflow.set_tag('Developer', '🅱🅻🅰🆀')
        if 'image' in request.files:
            file = request.files['image']
            image = Image.open(file)
            pred = predict(image)
            label_index = np.argmax(pred)
            label = labels[label_index]
            # Log the image and prediction to MLflow
            mlflow.log_artifact('image.jpg', 'image')
            mlflow.log_param('Prediction', label)
            mlflow.log_artifact( 'HARmodel_main.h5','tensorflow_VGG16_model')
      

            return jsonify({'prediction': label})
        else:
            return jsonify({'error': 'No image file found in the request.'}), 400
     
    
        
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
