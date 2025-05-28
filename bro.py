import onnx

# Load your original ONNX model
model = onnx.load("yolov4-tiny-single-batch.onnx")

# Names of reshape nodes we want to remove
reshape_nodes_to_remove = [
    "030_convolutional_reshape_1",
    "030_convolutional_reshape_2",
    "037_convolutional_reshape_1",
    "037_convolutional_reshape_2"
]

# Filter out those reshape nodes
new_nodes = [
    node for node in model.graph.node
    if node.name not in reshape_nodes_to_remove
]

# Clear and replace the graph's nodes list
del model.graph.node[:]
model.graph.node.extend(new_nodes)

# Save the patched model
onnx.save(model, "yolov4-tiny-fixed.onnx")
print("✅ Removed Reshape nodes and saved as yolov4-tiny-fixed.onnx")