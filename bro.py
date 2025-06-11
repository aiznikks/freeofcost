import tensorflow as tf

# Your frozen .pb path
frozen_graph_path = "resnet_v1_50.pb"

# Known tensor details — adjust if needed
input_arrays = ["InputImage"]               # From Netron
output_arrays = ["resnet_v1_50/predictions/Softmax"]  # Try to find this from Netron
input_shapes = {"InputImage": [1, 224, 224, 3]}        # Static shape

converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    frozen_graph_path,
    input_arrays=input_arrays,
    output_arrays=output_arrays,
    input_shapes=input_shapes
)

tflite_model = converter.convert()

with open("resnet_v1_50_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)