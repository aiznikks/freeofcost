import tensorflow as tf

# Load the static saved model
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model_static")

# Ensure it's a float32 model (no quantization)
converter.optimizations = []  # don't quantize

# Convert
tflite_model = converter.convert()

# Save it
with open("centernet_static_fp32.tflite", "wb") as f:
    f.write(tflite_model)