import tensorflow as tf
import numpy as np

# Representative dataset for calibration
def representative_dataset():
    for _ in range(100):
        dummy = np.random.randint(0, 256, size=(1, 300, 300, 3), dtype=np.uint8)
        yield [dummy]

# Create converter
converter = tf.lite.TFLiteConverter.from_saved_model("face_ssd_saved_model")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset

# Fix input shape
converter.resize_input_tensor(0, [1, 300, 300, 3])

# Set INT8 quantization (backbone INT8, input/output uint8 safest)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
    tf.lite.OpsSet.TFLITE_BUILTINS
]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Convert
tflite_model = converter.convert()

# Save
with open("face_ssd_mobilenetv1_int8_fixed.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite model generated: face_ssd_mobilenetv1_int8_fixed.tflite")