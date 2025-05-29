import tensorflow as tf
import numpy as np

# Path to your SavedModel
saved_model_dir = "saved_model_dir"

# 1. Create TFLite converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# 2. Resize input to fixed shape required for PTQ
converter.resize_input_tensor(0, [1, 300, 300, 3])  # SSD MobileNet standard input

# 3. Set optimization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 4. Provide a representative dataset for calibration (INT8 activation scaling)
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.randint(0, 256, size=(1, 300, 300, 3), dtype=np.uint8)
        yield [dummy_input]

converter.representative_dataset = representative_data_gen

# 5. Set input and output types for full INT8 model
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# 6. Convert model
tflite_model = converter.convert()

# 7. Save model
with open("ssd_mobilenet_v1_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ INT8 TFLite model saved as ssd_mobilenet_v1_int8.tflite")