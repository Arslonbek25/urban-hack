# "xray-classifier.h5"
# url  = "https://drive.google.com/drive/folders/1-LOth6pj_A-pTAra1czXxb8LuP7HvTtu"

import pickle
import numpy as np
import tensorflow as tf
import PIL
import os
from keras.models import load_model

# from flask import Flask, request, jsonify

# Load your pickled model
current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "models/xray_classifier-0.1.0.pkl")
print("CURRENT DIR", current_dir)
# with open(file_path, "rb") as model_file:
#     model = pickle.load(model_file)

# app = Flask(name)
model = load_model(os.path.join(current_dir, "models", "xray-classifier.h5"))
CLASS_NAMES = [
    "Atelectasis",
    "Cardiomegaly",
    "Effusion",
    "Infiltrate",
    "Mass",
    "Nodule",
    "Pneumonia",
    "Pneumothorax",
    "No Finding",
]


# @app.route("/predict", methods=["POST"])
def predict(image):
    try:
        # Ensure that the request contains an image file
        # if "image" not in request.files:
        #     return "No image file in the request", 400

        # Get the image file from the request
        image_file = image
        # image_file = request.files["image"]

        # Load and preprocess the image
        img = tf.keras.preprocessing.image.load_img(image_file)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.image.resize(img, (256, 256))  # Corrected the resize function
        img = tf.reshape(img, (-1, 256, 256, 3))
        img = img / 255.0  # Normalize pixel values

        # Make predictions using your model
        prediction = model.predict(img)

        # Return the class with the highest probability
        predicted_class = np.argmax(prediction)

        return CLASS_NAMES[int(predicted_class)]
        # return jsonify({"predicted_class": int(predicted_class)})

    except Exception as e:
        return str(e), 400


# if name == 'main':
#     app.run(host='0.0.0.0', port=5000)
