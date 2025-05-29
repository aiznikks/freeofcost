import tensorflow as tf
import numpy as np

# Path to your TF2 saved model
saved_model_dir = "ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8/saved_model"

# Create the converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Enable PTQ
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# Dummy representative dataset for calibration (matches input shape)
def representative_data_gen():
    for _ in range(100):
        yield [np.random.rand(1, 640, 640, 3).astype(np.float32)]

converter.representative_dataset = representative_data_gen

# Convert the model
tflite_model = converter.convert()

# Save it
with open("ssd_mobilenet_v1_fpn_640x640_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ PTQ done. INT8 TFLite model saved.")