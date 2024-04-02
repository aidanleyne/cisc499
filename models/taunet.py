import tensorflow as tf
import tensorflow_addons as tfa
import os
import numpy as np

recreated_model = tf.keras.Sequential([
    tf.keras.layers.LSTM(256, input_shape=(None, 1)),
    tf.keras.layers.Dense(128, activation=None),
    tf.keras.layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1))
])

recreated_model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tfa.losses.TripletSemiHardLoss()
)

#load-in model weights
filename = os.path.join(os.path.dirname(__file__), 'weights/taunet.h5')
recreated_model.load_weights(filename)

def generate(filepath):
    data = _read_text_files(filepath)
    return recreated_model.predict(data)[0]

def _read_text_files(filepath):
    # Read the contents of the file, skipping the first line
    with open(filepath, 'r') as file:
        lines = file.readlines()[1:]  # Skip the "TIME_DELTA" line
        keystrokes = [int(line.strip()) for line in lines]  # Convert to integers
    
    return  np.array(keystrokes).astype('int32').reshape(1, -1)