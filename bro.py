import tensorflow as tf

# Path to your SavedModel directory
saved_model_dir = "saved_model_dir"  # update if different
tflite_output_path = "resnet_v2_50_fp32_static.tflite"

# Set input details (usually resnet input is 224x224x3)
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.target_spec.supported_types = [tf.float32]
converter.experimental_new_converter = True
converter.allow_custom_ops = True
converter.optimizations = []

# Force static input shape if it's dynamic
converter._experimental_disable_batchmatmul_unfold = True
converter.experimental_fixed_shape_representation = True

# Optional but safe to add: set static input shape
def representative_dataset_gen():
    for _ in range(1):
        yield [tf.random.uniform([1, 224, 224, 3], dtype=tf.float32)]

converter.representative_dataset = representative_dataset_gen

# Convert
tflite_model = converter.convert()

# Save
with open(tflite_output_path, "wb") as f:
    f.write(tflite_model)