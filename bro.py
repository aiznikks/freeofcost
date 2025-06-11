import tensorflow as tf

# Use static FP32 model as base
fp32_model_path = "inception_v3_fp32_static.tflite"

# Load the model
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model_dir")  # safer to re-load from original
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Set INT8 as target
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Set fixed shape: [1, 299, 299, 3]
def representative_dataset():
    for _ in range(100):
        yield [tf.random.uniform([1, 299, 299, 3], 0, 255, dtype=tf.float32)]

converter.representative_dataset = representative_dataset

# Convert and save
int8_model = converter.convert()
with open("inception_v3_int8_static.tflite", "wb") as f:
    f.write(int8_model)