import onnx

model = onnx.load("yolov4-tiny-single-batch.onnx")

reshape_names_to_remove = [
    "030_convolutional_reshape_1",
    "030_convolutional_reshape_2",
    "037_convolutional_reshape_1",
    "037_convolutional_reshape_2"
]

# Remove Reshape Nodes
model.graph.node[:] = [node for node in model.graph.node if node.name not in reshape_names_to_remove]

# Remove Shape Initializers (like '030_convolutional_shape', etc.)
shape_initializers_to_remove = [
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape"
]

model.graph.initializer[:] = [init for init in model.graph.initializer if init.name not in shape_initializers_to_remove]
model.graph.input[:] = [i for i in model.graph.input if i.name not in shape_initializers_to_remove]

onnx.save(model, "yolov4-tiny-clean.onnx")
print("✅ Reshape nodes and their shape initializers removed. Saved as yolov4-tiny-clean.onnx")