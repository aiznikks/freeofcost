import tensorflow as tf

# Load SavedModel
model = tf.saved_model.load("saved_model_dir")
concrete_func = model.signatures["serving_default"]

# Force the input shape to be static
concrete_func.inputs[0].set_shape([1, 224, 224, 3])

# Convert using concrete function
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Provide dummy representative dataset for PTQ
def representative_dataset():
    for _ in range(100):
        yield [tf.random.uniform([1, 224, 224, 3], minval=0, maxval=255, dtype=tf.float32)]

converter.representative_dataset = representative_dataset

# Convert the model
tflite_model = converter.convert()

# Save the final model
with open("mobilenet_v1_int8_static.tflite", "wb") as f:
    f.write(tflite_model)
    
    
    
#
import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path="mobilenet_v1_int8.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
print(input_details[0]['dtype'], input_details[0]['quantization'])

