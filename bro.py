import tensorflow as tf

# Load MobileNetV2 SavedModel
model = tf.saved_model.load("mobilenet_v2_saved_model")  # change path as needed
concrete_func = model.signatures["serving_default"]

# Set static input shape
concrete_func.inputs[0].set_shape([1, 224, 224, 3])  # Static input for MobileNetV2

# Convert to FP32 .tflite
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.optimizations = []  # Keep it FP32
converter.target_spec.supported_types = [tf.float32]

tflite_model = converter.convert()

# Save the model
with open("mobilenet_v2_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)