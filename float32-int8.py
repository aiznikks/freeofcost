import tensorflow as tf
import numpy as np

# Path to SavedModel
saved_model_dir = "ssd_mobilenet_v1_coco_2018_01_28/saved_model"
tflite_model_path = "ssd_mobilenet_v1_int8.tflite"

# Representative dataset
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 300, 300, 3).astype(np.float32)
        yield [dummy_input]

# Load and convert
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# Convert and save
tflite_model = converter.convert()
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

print("✅ Saved INT8 TFLite model at:", tflite_model_path)
