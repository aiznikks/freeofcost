import tensorflow as tf
import numpy as np

# Representative dataset generator
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 300, 300, 3).astype(np.float32)
        yield [dummy_input]

# Paths
pb_model_path = "ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb"
tflite_model_path = "ssd_mobilenet_v1_int8.tflite"

# Input/output names (you can verify in Netron)
input_arrays = ["image_tensor"]
output_arrays = ["detection_boxes", "detection_scores", "detection_classes", "num_detections"]
input_shapes = {"image_tensor": [1, 300, 300, 3]}

# Conversion setup
converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    pb_model_path,
    input_arrays=input_arrays,
    output_arrays=output_arrays,
    input_shapes=input_shapes
)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Convert and save model
tflite_model = converter.convert()
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print("INT8 TFLite model saved at:", tflite_model_path)
