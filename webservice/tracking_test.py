import shutil
import requests


# URL of the Flask app
URL = 'http://localhost:9696/tracking_predict'

# Image URL for prediction
IMAGE_URL = 'https://www.choc.org/wp/wp-content/uploads/2019/08/kid-drinking-water.jpg'

# Download the image and save it locally
IMAGE_PATH = 'webservice/image.jpg'
response = requests.get(IMAGE_URL, stream=True, timeout=None)
with open(IMAGE_PATH, 'wb') as file:
    shutil.copyfileobj(response.raw, file)

# Send a POST request with the image file
response = requests.post(URL, files={'image': open(IMAGE_PATH, 'rb')},timeout=None)

# Check the response status code
if response.status_code == 200:
    # Retrieve the prediction result
    result = response.json()
    prediction = result['prediction']
    print("Prediction:", prediction)
else:
    print('Error occurred during prediction.')
