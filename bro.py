import tensorflow as tf
import numpy as np

# Path to your SSD MobileNet V1 SavedModel directory
saved_model_dir = "ssd_mobilenet_v1/saved_model"

# Representative dataset for calibration
def representative_data_gen():
    for _ in range(100):
        data = np.random.rand(1, 300, 300, 3).astype(np.float32)
        yield [data]

# Create converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen

# Explicitly prevent TFLite from changing I/O types
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,        # For float ops
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8    # For int8 weights
]

# Do NOT force inference_input/output_type

# Convert model
tflite_model = converter.convert()

# Save to file
with open("ssd_mobilenet_v1_quantized_float_io.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Conversion done: ssd_mobilenet_v1_quantized_float_io.tflite")