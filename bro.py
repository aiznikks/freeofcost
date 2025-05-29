import onnx

# Load the broken model
model = onnx.load("yolov4-tiny-clean.onnx")

# Problem shape names
shape_names_to_remove = [
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape"
]

# Step 1: Remove nodes that reference any of those as input
clean_nodes = []
for node in model.graph.node:
    if not any(shape in node.input for shape in shape_names_to_remove):
        clean_nodes.append(node)

model.graph.ClearField("node")
model.graph.node.extend(clean_nodes)

# Step 2: Remove those names from initializers
model.graph.initializer[:] = [
    init for init in model.graph.initializer
    if init.name not in shape_names_to_remove
]

# Step 3: Remove from graph inputs
model.graph.input[:] = [
    i for i in model.graph.input
    if i.name not in shape_names_to_remove
]

# Step 4: Double-check no node still references it
for node in model.graph.node:
    for name in shape_names_to_remove:
        assert name not in node.input, f"🚨 Node still references {name}"

# Save cleaned model
onnx.save(model, "yolov4-tiny-ultraclean.onnx")
print("✅ Saved as yolov4-tiny-ultraclean.onnx — no broken references remain.")