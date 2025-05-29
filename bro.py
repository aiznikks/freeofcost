import onnx

# Load model
model = onnx.load("yolov4-tiny-fullyclean.onnx")

# Set of all problem tensor names
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

# 1. Remove any nodes using these names
model.graph.node[:] = [n for n in model.graph.node if all(inp not in offending_names for inp in n.input)]

# 2. Remove initializers
model.graph.initializer[:] = [i for i in model.graph.initializer if i.name not in offending_names]

# 3. Remove inputs
model.graph.input[:] = [i for i in model.graph.input if i.name not in offending_names]

# 4. Remove from value_info (optional metadata)
model.graph.value_info[:] = [v for v in model.graph.value_info if v.name not in offending_names]

# 5. Save cleaned model
onnx.save(model, "yolov4-tiny-finalfinal.onnx")
print("✅ Saved as yolov4-tiny-finalfinal.onnx — all shape references are gone")