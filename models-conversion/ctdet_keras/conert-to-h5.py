import tensorflow as tf

# Enable TF1 compatibility mode
tf.compat.v1.disable_eager_execution()

frozen_graph_path = "ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb"

# Setup converter using TF1 frozen graph
converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
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

# Apply weight-only quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert the model
tflite_model = converter.convert()

# Save the TFLite file
with open("ssd_mobilenet_v1_dynamic_quant.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Done: Quantized model saved as ssd_mobilenet_v1_dynamic_quant.tflite")