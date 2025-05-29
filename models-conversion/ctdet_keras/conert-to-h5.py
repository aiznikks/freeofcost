import tensorflow as tf

# Path to your TF1 frozen graph
frozen_graph_path = "ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb"

# TFLite converter setup for frozen graph
converter = tf.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file=frozen_graph_path,
    input_arrays=["image_tensor"],
    input_shapes={"image_tensor": [1, 300, 300, 3]},
    output_arrays=[
        "detection_boxes",
        "detection_scores",
        "detection_classes",
        "num_detections"
    ]
)

# Enable dynamic range quantization (weights only)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert model
tflite_model = converter.convert()

# Save it
with open("ssd_mobilenet_v1_weights_quant.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Converted with weight-only quantization.")