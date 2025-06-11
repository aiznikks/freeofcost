import tensorflow as tf

# Load SavedModel
saved_model_dir = "saved_model_dir"  # path to your inceptionv3 saved model
model = tf.saved_model.load(saved_model_dir)
concrete_func = model.signatures["serving_default"]

# Force input to static shape [1, 299, 299, 3]
concrete_func.inputs[0].set_shape([1, 299, 299, 3])

# Build converter from this fixed concrete function
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

# Static + PTQ
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Provide representative dataset
def representative_dataset():
    for _ in range(100):
        yield [tf.random.uniform([1, 299, 299, 3], 0, 255, dtype=tf.float32)]

converter.representative_dataset = representative_dataset

# Convert
int8_model = converter.convert()

# Save model
with open("inception_v3_int8_static.tflite", "wb") as f:
    f.write(int8_model)