import tensorflow as tf
import numpy as np

# Path to your SavedModel directory (not the .pb file)
saved_model_dir = "ssd_mobilenet_v1/saved_model"  # adjust if needed

# Define dummy input similar to real input (for calibration)
def representative_data_gen():
    for _ in range(100):
        yield [np.random.rand(1, 300, 300, 3).astype(np.float32)]

# Load converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Enable optimization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Provide representative dataset
converter.representative_dataset = representative_data_gen

# Allow both float and int8 ops to prevent input type mismatch
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,         # float ops (for I/O)
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8     # int8 weights/internal
]

# DO NOT SET inference_input_type / inference_output_type

# Convert
tflite_model = converter.convert()

# Save model
with open("ssd_mobilenet_v1_int8_float_io.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Conversion successful!")