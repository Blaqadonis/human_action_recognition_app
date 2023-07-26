import sys
import requests
import shutil


def run():
    '''run function'''
    image_url = sys.argv[1]  # # Image URL for prediction
    # URL of the Flask app
    url = 'http://localhost:9696/predict'

    # Download the image and save it locally
    image_path = 'image.jpg'
    response = requests.get(image_url, stream=True)
    with open(image_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    # Send a POST request with the image file
    response = requests.post(url, files={'image': open(image_path, 'rb')})

    # Check the response status code
    if response.status_code == 200:
        # Retrieve the prediction result
        result = response.json()
        prediction = result['prediction']
        print("Prediction:", prediction)
    else:
        print('Error occurred during prediction.')
    
    return 

if __name__ == '__main__':
    run()
    
    
