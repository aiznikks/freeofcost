import tensorflow as tf
import numpy as np

# 1. Load the SavedModel and inspect input name
model = tf.saved_model.load("unet_saved_model")
input_name = list(model.signatures["serving_default"].structured_input_signature[1].keys())[0]
print("Model input name:", input_name)

# 2. Representative dataset
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 128, 128, 16).astype(np.float32)
        yield [dummy_input]

# 3. Convert to INT8 TFLite model
converter = tf.lite.TFLiteConverter.from_saved_model("unet_saved_model")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# 4. Force fixed input shape (to avoid ResizeInputTensorStrict error)
converter._experimental_disable_batch_size = True
converter.resize_input_shape = {input_name: [1, 128, 128, 16]}

# 5. Convert and save
tflite_model = converter.convert()
with open("unet_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("INT8 TFLite model saved as: unet_int8.tflite")