import tensorflow as tf
import numpy as np

# Path to your SSD MobileNet V1 SavedModel
saved_model_dir = "ssd_mobilenet_v1/saved_model"  # change this if needed

# Representative dataset generator
def representative_data_gen():
    for _ in range(100):
        # Shape must match model input, often [1, 300, 300, 3] for SSD MobileNet
        dummy_input = np.random.rand(1, 300, 300, 3).astype(np.float32)
        yield [dummy_input]

# Create converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen

# Do not set input/output type for float32 I/O
# This allows INT8 weights/activations but keeps input/output in float

# Convert
tflite_model = converter.convert()

# Save to .tflite file
with open("ssd_mobilenet_v1_int8_float_io.tflite", "wb") as f:
    f.write(tflite_model)

print("Conversion completed: ssd_mobilenet_v1_int8_float_io.tflite")