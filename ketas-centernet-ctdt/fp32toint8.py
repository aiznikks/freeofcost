import tensorflow as tf
import numpy as np

# Load original saved model (not .tflite)
converter = tf.lite.TFLiteConverter.from_saved_model("path_to_saved_model")

# Set optimizations
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Provide a representative dataset
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 512, 512, 3).astype(np.float32)
        yield [dummy_input]

converter.representative_dataset = representative_data_gen

# Force full integer quantization
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8  # or tf.int8
converter.inference_output_type = tf.int8  # or tf.int8

# Convert and save
tflite_model = converter.convert()
with open("centernet_int8.tflite", "wb") as f:
    f.write(tflite_model)