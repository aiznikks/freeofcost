import tensorflow as tf
import numpy as np

def representative_data_gen():
    for _ in range(100):
        yield [np.random.rand(1, 128, 128, 16).astype(np.float32)]

converter = tf.lite.TFLiteConverter.from_saved_model("unet_saved_model_fixed")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()
with open("unet_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("INT8 model ready: unet_int8.tflite")
