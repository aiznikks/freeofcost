import onnx

# Load model
model = onnx.load("yolov4-tiny-fullyclean.onnx")

# Offending tensors/nodes to remove
offending_names = {
    "030_convolutional_shape",
    "030_convolutional_transpose_shape",
    "037_convolutional_shape",
    "037_convolutional_transpose_shape",
    "030_convolutional_reshape_1",
    "030_convolutional_reshape_2",
    "037_convolutional_reshape_1",
    "037_convolutional_reshape_2"
}

# Step 1: Clean nodes
clean_nodes = [n for n in model.graph.node if all(inp not in offending_names for inp in n.input)]
model.graph.ClearField("node")
model.graph.node.extend(clean_nodes)

# Step 2: Clean initializers
clean_init = [i for i in model.graph.initializer if i.name not in offending_names]
model.graph.ClearField("initializer")
model.graph.initializer.extend(clean_init)

# Step 3: Clean inputs
clean_inputs = [i for i in model.graph.input if i.name not in offending_names]
model.graph.ClearField("input")
model.graph.input.extend(clean_inputs)

# Step 4: Clean value_info (optional metadata)
clean_values = [v for v in model.graph.value_info if v.name not in offending_names]
model.graph.ClearField("value_info")
model.graph.value_info.extend(clean_values)

# Save model
onnx.save(model, "yolov4-tiny-finalfinal.onnx")
print("✅ Saved as yolov4-tiny-finalfinal.onnx — every reference is purged")