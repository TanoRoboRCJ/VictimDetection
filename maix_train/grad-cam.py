import numpy as np
import tensorflow as tf
from tensorflow import keras

import os
import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os
import cv2

import shutil

def load_image(path, target_size=(224, 224)):
    img = image.load_img(path, target_size=target_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def grad_cam(input_model, image, cls, layer_name):
    with tf.GradientTape() as tape:
        last_conv_layer = input_model.get_layer(layer_name)
        iterate = tf.keras.models.Model([input_model.inputs], [input_model.output, last_conv_layer.output])
        model_out, last_conv_layer = iterate(image)
        class_out = model_out[:, np.argmax(model_out[0])]
        grads = tape.gradient(class_out, last_conv_layer)
        pooled_grads = K.mean(grads, axis=(0, 1, 2))
        
    heatmap = tf.reduce_mean(tf.multiply(pooled_grads, last_conv_layer), axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    return heatmap

model = keras.models.load_model('out/m.tflite.h5')
model.summary()
layer_name = 'conv_pw_13_relu'  # MobileNetの最後の畳み込み層

def overlay_heatmap_on_image(image, heatmap):
    heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * 0.4 + image
    return superimposed_img

image_dir = 'out/sample_images'
image_files = os.listdir(image_dir)

out_dir = 'out/heatmap/'
# os.makedirs(out_dir, exist_ok=True)
# すでにある場合はour_dirを一旦消す
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

os.makedirs(out_dir)

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    img = load_image(image_path)

    preds = model.predict(img)
    cls = np.argmax(preds)

    cam = grad_cam(model, img, cls, layer_name)
    cam = np.squeeze(cam)  # 余分な次元を削除

    img = cv2.imread(image_path)
    INTENSITY = 0.6

    cam = cv2.resize(cam, (img.shape[1], img.shape[0]))
    cam = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)

    img = img * (1.0 - INTENSITY) + cam * INTENSITY

    out_path = os.path.join(out_dir, image_file)
    cv2.imwrite(out_path, img)