import tensorflow as tf

# Load the SavedModel
model_dir = "saved_model_dir"  # Replace with actual path if different
model = tf.saved_model.load(model_dir)

# Get concrete function
concrete_func = model.signatures["serving_default"]

# Set input shape to static
concrete_func.inputs[0].set_shape([1, 299, 299, 3])  # InceptionV3 expects 299x299 input

# Create TFLiteConverter from the fixed-shape function
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.target_spec.supported_types = [tf.float32]
converter.optimizations = []  # No quantization, keep FP32
converter.inference_input_type = tf.float32
converter.inference_output_type = tf.float32

# Convert and save
tflite_model = converter.convert()
with open("inception_v3_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)