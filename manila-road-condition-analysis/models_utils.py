import os
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# Load CNN model
def load_cnn_model(model_path='road_condition_model.h5'):
    model = load_model(model_path)
    return model

# Predict road conditions using the CNN model
def predict_road_conditions(model, image_dir='road_images'):
    conditions = []

    for image_file in os.listdir(image_dir):
        img_path = os.path.join(image_dir, image_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (128, 128))  # size as per model's requirement
        img = img.astype('float32') / 255.0  # Normalize
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)
        condition = np.argmax(pred)  #  outputs class probabilities
        conditions.append(condition)

    return conditions
