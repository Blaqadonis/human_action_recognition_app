import os
import pytest
from PIL import Image
from predict import preprocess_image, predict
p

def test_preprocess_image():
    '''Test preprocessing function'''
    image = Image.new('RGB', (160, 160))
    preprocessed_image = preprocess_image(image)
    assert preprocessed_image.shape == (160, 160, 3)


def test_predict():
    '''Test prediction function'''
    image = Image.new('RGB', (160, 160))
    prediction = predict(image)
    assert 0 <= prediction[0] <= 1  # Ensure prediction values are between 0 and 1

if __name__ == "__main__":
    pytest.main()
