import onnx

# Load the model
model = onnx.load("yolov4-tiny-clean.onnx")

# These are known problematic initializers and reshape references
shape_names_to_remove = [
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape"
]

# Step 1: Remove nodes that use these as inputs
filtered_nodes = []
for node in model.graph.node:
    if not any(shape in node.input for shape in shape_names_to_remove):
        filtered_nodes.append(node)

# Step 2: Remove any leftover initializers with those names
filtered_initializers = [
    init for init in model.graph.initializer
    if init.name not in shape_names_to_remove
]

# Step 3: Remove input tensors that reference those names
filtered_inputs = [
    inp for inp in model.graph.input
    if inp.name not in shape_names_to_remove
]

# Apply all the filtered components
del model.graph.node[:]
model.graph.node.extend(filtered_nodes)

del model.graph.initializer[:]
model.graph.initializer.extend(filtered_initializers)

del model.graph.input[:]
model.graph.input.extend(filtered_inputs)

# Save it clean
onnx.save(model, "yolov4-tiny-fullyclean.onnx")
print("✅ Fully cleaned model saved as yolov4-tiny-fullyclean.onnx")