import tensorflow as tf
import numpy as np

# Path to unpacked float32 SavedModel
saved_model_dir = "ssd_mobilenet_v1_640x640_coco17_tpu-8/saved_model"

# 1. Create converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 2. Set input/output to int8
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# 3. Provide representative dataset
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 640, 640, 3).astype(np.float32)
        yield [dummy_input]

converter.representative_dataset = representative_data_gen

# 4. Convert
tflite_model = converter.convert()

# 5. Save
with open("ssd_mobilenet_v1_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ PTQ done: ssd_mobilenet_v1_int8.tflite saved.")