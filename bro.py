import onnx

# Load model
model = onnx.load("yolov4-tiny-single-batch.onnx")

# Reshape nodes to remove
reshape_nodes_to_remove = [
    "030_convolutional_reshape_1",
    "030_convolutional_reshape_2",
    "037_convolutional_reshape_1",
    "037_convolutional_reshape_2"
]

# Shape initializers to remove
shape_initializers_to_remove = [
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape"
]

# Remove reshape nodes
filtered_nodes = []
for node in model.graph.node:
    if node.name not in reshape_nodes_to_remove:
        filtered_nodes.append(node)
del model.graph.node[:]
model.graph.node.extend(filtered_nodes)

# Remove initializers
filtered_inits = []
for init in model.graph.initializer:
    if init.name not in shape_initializers_to_remove:
        filtered_inits.append(init)
del model.graph.initializer[:]
model.graph.initializer.extend(filtered_inits)

# Remove inputs that match those initializers
filtered_inputs = []
for inp in model.graph.input:
    if inp.name not in shape_initializers_to_remove:
        filtered_inputs.append(inp)
del model.graph.input[:]
model.graph.input.extend(filtered_inputs)

# Save patched model
onnx.save(model, "yolov4-tiny-clean.onnx")
print("✅ Clean model saved as yolov4-tiny-clean.onnx")