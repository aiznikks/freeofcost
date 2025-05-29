import onnx

model = onnx.load("yolov4-tiny-fullyclean.onnx")

# Explicitly remove these reshape nodes
reshape_nodes_to_remove = [
    "030_convolutional_reshape_1",
    "030_convolutional_reshape_2",
    "037_convolutional_reshape_1",
    "037_convolutional_reshape_2"
]

# Remove nodes by name
remaining_nodes = [n for n in model.graph.node if n.name not in reshape_nodes_to_remove]
model.graph.ClearField("node")
model.graph.node.extend(remaining_nodes)

# Save final clean model
onnx.save(model, "yolov4-tiny-int8-ready.onnx")
print("✅ Removed last reshape nodes. Saved as yolov4-tiny-int8-ready.onnx")