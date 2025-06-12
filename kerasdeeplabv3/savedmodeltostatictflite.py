import tensorflow as tf

# Path to your DeepLabV3+ SavedModel
saved_model_dir = "path/to/saved_model_dir"

# Create the TFLite converter
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Set fixed static input shape
converter.experimental_new_converter = True
converter.allow_custom_ops = True
converter._experimental_shape_signature = [tf.TensorShape([1, 512, 512, 3])]

# Keep FP32 (no quantization)
converter.optimizations = []
converter.inference_input_type = tf.float32
converter.inference_output_type = tf.float32

# Convert and save
tflite_model = converter.convert()
with open("deeplabv3p_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)