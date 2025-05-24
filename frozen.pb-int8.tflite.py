import tensorflow as tf
import numpy as np

# Path to your frozen .pb model
pb_model_path = "frozen_inference_graph_face.pb"

# Create the converter
converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file=pb_model_path,
    input_arrays=["image_tensor"],
    output_arrays=[
        "detection_boxes",
        "detection_scores",
        "detection_classes",
        "num_detections"
    ],
    input_shapes={"image_tensor": [1, 300, 300, 3]}
)

# Set optimization flag
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Define representative dataset generator (needed for INT8 quantization)
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.randint(0, 256, size=(1, 300, 300, 3), dtype=np.uint8)
        yield [dummy_input]

converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Force input/output to be INT8
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Convert the model
tflite_model = converter.convert()

# Save the converted model
with open("face_detector_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("INT8 conversion complete. Saved as face_detector_int8.tflite")
