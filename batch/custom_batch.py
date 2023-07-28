import os
import sys
import uuid
import pandas as pd
import numpy as np
from tensorflow import keras
from prefect import task, flow, get_run_logger
from PIL import Image
from prefect_email import EmailServerCredentials, email_send_message
from prefect.artifacts import create_markdown_artifact
from datetime import date

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

    predictions_mapped = [label_map[prediction] for prediction in predictions]

    predictions_df = pd.DataFrame({"ID": [str(uuid.uuid4()) for _ in range(len(predictions_mapped))],
                                "prediction": predictions_mapped})
    predictions_df['model_version'] = run_id
    predictions_df.to_csv(output_file, index=False)
    

@task(retries=3, retry_delay_seconds=2, name="Apply HAR Model")
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

    markdown__prediction_report = f"""# Batch Testing_set.csv Prediction Report

        ## Summary

        Duration Prediction 

        ## TensorFlow Model

        | On    | 
        |:----------|-------:|
        | {date.today()} | 
        """

    create_markdown_artifact(
            key="batch-testing-prediction-report", markdown=markdown__prediction_report
        )

    return output_file






@flow
def send_update(block: str, email_address: str, password: str):
    '''Notify the ML engineer'''
    credentials = EmailServerCredentials(
    username=email_address,
    password=password,  # must be an app password
    )
    credentials.save(block, overwrite=True)
    email_server_credentials = EmailServerCredentials.load(block)
    email_send_message.with_options(name=f"email {email_address}").submit(
    email_server_credentials=email_server_credentials,
    subject="Batch Testing Run Status",
    msg="Run completed!!",
    email_to=email_address,
        )

@flow
def run():
    '''run function'''
    csv_file = sys.argv[1]  # 'Testing_set.csv'
    run_id = sys.argv[2]  # 'MLflow Run ID'
    block = sys.argv[3]   #'update-me'
    email = sys.argv[4]   #'your-email-address'
    password = sys.argv[5]  #'your-app-password'
    output_file = '{sys.argv[6]}/result.csv' # 'output-file-path'
    apply_model(csv_file=csv_file, run_id=run_id, output_file=output_file)
    send_update(block=block, email_address=email, password=password)
    return print('Run completed! Status sent to your email.')

if __name__ == '__main__':
    run()
