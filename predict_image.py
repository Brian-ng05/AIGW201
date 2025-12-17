import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import matplotlib.pyplot as plt

MODEL_PATH = os.path.join("worms_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

classes = ["cabbage worm", "corn earworm", "cutworm", "fall armyworm"]

def predict_image(img_path, threshold=0.5):
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    confidence = float(predictions[0][class_index])

    plt.imshow(image.load_img(img_path))
    plt.axis("off")
    plt.show()

    if confidence < threshold:
        return ""
    else:
        return f"{classes[class_index]}"
    
