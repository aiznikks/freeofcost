import tensorflow as tf
import numpy as np

# Load the original FP32 saved_model
converter = tf.lite.TFLiteConverter.from_saved_model("ssd_mobilenet_v1_fp32_saved_model")

# Set optimization for INT8 quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Set representative dataset for calibration
def representative_dataset():
    for _ in range(100):
        yield [np.random.rand(1, 320, 320, 3).astype(np.float32)]

converter.representative_dataset = representative_dataset

# Enforce full INT8 quantization (inputs and outputs too)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8   # or tf.int8 depending on hardware
converter.inference_output_type = tf.int8

# Convert the model
tflite_model = converter.convert()

# Save the static int8 model
with open("ssd_mobilenet_v1_320x320_int8_static.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Saved static INT8 TFLite with shape [1, 320, 320, 3]")