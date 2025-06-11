import tensorflow as tf

# Load the SavedModel
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model_dir")

# Set static input shape — common for MobileNetV1 is (1, 224, 224, 3)
# Only needed if the model has dynamic input defined in the graph

converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Specify INT8 inference (fully quantized model)
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Provide representative dataset for calibration
def representative_dataset():
    for _ in range(100):
        # Fake data in uint8 [0, 255] scaled to float32 [0.0, 1.0] if needed
        yield [tf.random.uniform(shape=[1, 224, 224, 3], minval=0, maxval=255, dtype=tf.float32)]

converter.representative_dataset = representative_dataset

# Convert
tflite_model = converter.convert()

# Save the static model
with open("mobilenet_v1_int8_static.tflite", "wb") as f:
    f.write(tflite_model)