import tensorflow as tf
import numpy as np

# Load the newly exported FP32 SavedModel
converter = tf.lite.TFLiteConverter.from_saved_model("exported_model_dir/saved_model")
converter.optimizations = [tf.lite.Optimize.DEFAULT]

def representative_dataset():
    for _ in range(100):
        yield [np.random.rand(1, 320, 320, 3).astype(np.float32)]  # adjust shape if needed

converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()

with open("ssd_mobilenet_v1_int8_static.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Done: Fully static int8 model saved.")