import tensorflow as tf
import numpy as np

# Representative dataset for calibration
def representative_dataset():
    for _ in range(100):
        dummy = np.random.randint(0, 256, size=(1, 300, 300, 3), dtype=np.uint8)
        yield [dummy]

# Convert from FROZEN GRAPH — this works 100% in TF1.15
converter = tf.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file="model.pb",
    input_arrays=["image_tensor"],
    input_shapes={"image_tensor": [1, 300, 300, 3]},
    output_arrays=[
        "detection_boxes",
        "detection_scores",
        "detection_classes",
        "num_detections"
    ]
)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset

# INT8 backbone + fallback for post-process
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
    tf.lite.OpsSet.TFLITE_BUILTINS
]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Convert
tflite_model = converter.convert()

# Save
with open("face_ssd_mobilenetv1_int8_frozen.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ FROZEN GRAPH conversion done: face_ssd_mobilenetv1_int8_frozen.tflite")