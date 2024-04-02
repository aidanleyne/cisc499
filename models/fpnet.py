import os
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa

#select to silence or not
OUTPUT_STATUS = 0

# Recreate the model architecture
recreated_model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=24, kernel_size=(1,3), activation='relu', input_shape=(481, 600, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2)),
    tf.keras.layers.Conv2D(filters=32, kernel_size=(1,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(1,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(1,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=96, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=96, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(1,2), strides=(1,2), padding='same'),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation=None), # No activation on final dense layer
    tf.keras.layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1)) # L2 normalize embeddings
])
# Compile the recreated model
recreated_model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001, beta_1=.9, beta_2=.999),
    loss=tfa.losses.TripletSemiHardLoss()
)

# Load the weights
filename = os.path.join(os.path.dirname(__file__), 'weights/fpnet.h5')
recreated_model.load_weights(filename)

def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=1)
    image = tf.image.resize(image, [481, 600])
    image = tf.cast(image, tf.uint8)
    return image

def generate(filepath):
    img = preprocess_image(filepath)
    img = tf.expand_dims(img, axis=0)
    return recreated_model.predict(img, verbose=OUTPUT_STATUS)[0]