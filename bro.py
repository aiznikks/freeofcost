import tensorflow as tf

# Load your SavedModel
saved_model_dir = "saved_model_dir"  # update path if needed
model = tf.saved_model.load(saved_model_dir)

# Get the concrete function
concrete_func = model.signatures["serving_default"]

# Force static shape here
concrete_func.inputs[0].set_shape([1, 224, 224, 3])  # <- key step

# Convert using TFLiteConverter
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.target_spec.supported_types = [tf.float32]
converter.optimizations = []

tflite_model = converter.convert()

# Save the model
with open("resnet_v2_50_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)