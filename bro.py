import onnx

# Load the broken model
model = onnx.load("yolov4-tiny-clean.onnx")

# All shape-related troublemakers
shape_names_to_remove = [
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape"
]

# --- Step 1: Remove all nodes that reference those names as input ---
new_nodes = [
    node for node in model.graph.node
    if not any(bad_name in node.input for bad_name in shape_names_to_remove)
]
model.graph.ClearField("node")
model.graph.node.extend(new_nodes)

# --- Step 2: Remove those shape names from initializers ---
new_initializers = [
    init for init in model.graph.initializer
    if init.name not in shape_names_to_remove
]
model.graph.ClearField("initializer")
model.graph.initializer.extend(new_initializers)

# --- Step 3: Remove from model inputs ---
new_inputs = [
    inp for inp in model.graph.input
    if inp.name not in shape_names_to_remove
]
model.graph.ClearField("input")
model.graph.input.extend(new_inputs)

# --- Step 4: Assert no broken refs left ---
for node in model.graph.node:
    for bad in shape_names_to_remove:
        assert bad not in node.input, f"❌ Still references: {bad}"

# Save
onnx.save(model, "yolov4-tiny-ultraclean.onnx")
print("✅ Final model saved as yolov4-tiny-ultraclean.onnx — no broken reshape dependencies left.")