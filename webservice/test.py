import requests
import shutil

# URL of the Flask app
url = 'http://localhost:9696/predict'

# Image URL for prediction
image_url = 'https://i2-prod.mirror.co.uk/incoming/article29722623.ece/ALTERNATES/s390/0_GettyImages-1482509341.jpg'

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
