import tensorflow as tf
import numpy as np

# Representative dataset for calibration
def representative_dataset():
    for _ in range(100):
        dummy = np.random.randint(-128, 127, size=(1, 300, 300, 3), dtype=np.int8)
        yield [dummy]

# Create TFLite converter
converter = tf.lite.TFLiteConverter.from_saved_model("face_ssd_saved_model")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset

# Force FULL INT8 — input/output/int ops
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# Convert model
tflite_model = converter.convert()

# Save TFLite model
with open("face_ssd_mobilenetv1_full_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("FULL INT8 TFLite model generated: face_ssd_mobilenetv1_full_int8.tflite")