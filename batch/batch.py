import os
import sys
import uuid
import pandas as pd
import numpy as np
from tensorflow import keras
from prefect import task, flow, get_run_logger
from PIL import Image
from prefect_email import EmailServerCredentials, email_send_message

def load_model(run_id):
    '''Loading the model'''    
    model = keras.models.load_model('HARmodel_main.h5')
    return model

def read_predict(file_names, model):
    '''Reading and making predictions'''
    predictions = []
    test_folder = 'test'
    
    for file_name in file_names:
        file_path = os.path.join(test_folder, file_name)
        image = Image.open(file_path)
        image = image.resize((160, 160))
        image_array = np.asarray(image)
        image_array = np.expand_dims(image_array, axis=0)
        result = model.predict(image_array)
        prediction = np.argmax(result)
        predictions.append(prediction)
    
    return predictions

def save_results(predictions, run_id, output_file):
    '''Saving the results'''
    label_map = {
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

    predictions_mapped = [label_map[prediction] for prediction in predictions]

    predictions_df = pd.DataFrame({"ID": [str(uuid.uuid4()) for _ in range(len(predictions_mapped))],
                                "prediction": predictions_mapped})
    predictions_df['model_version'] = run_id
    predictions_df.to_csv(output_file, index=False)
    

@task
def apply_model(csv_file, run_id, output_file):
    '''Applying everything'''
    logger = get_run_logger()
    logger.info(f'Loading model...')
    model = load_model(run_id)
    logger.info(f'Reading and making predictions on data from {csv_file}...')
    data = pd.read_csv(csv_file)
    file_names = data['filename'].tolist()
    predictions = read_predict(file_names, model)
    logger.info(f'Saving the results to {output_file}...')
    save_results(predictions, run_id, output_file)
    return output_file


@flow
def run():
    '''run function'''
    csv_file = sys.argv[1]  # 'Testing_set.csv'
    run_id = sys.argv[2]  # 'your-MLflow-Run_id'
    output_file = 'batch/output/result.csv'
   
    apply_model(csv_file=csv_file, run_id=run_id, output_file=output_file)
    return print('Done!')

if __name__ == '__main__':
    run()
