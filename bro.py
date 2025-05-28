import onnx

model = onnx.load("yolov4-tiny-single-batch.onnx")

# Remove the 4 reshape nodes known to cause problems
model.graph.node[:] = [
    node for node in model.graph.node
    if node.name not in [
        "030_convolutional_reshape_1",
        "030_convolutional_reshape_2",
        "037_convolutional_reshape_1",
        "037_convolutional_reshape_2"
    ]
]

onnx.save(model, "yolov4-tiny-fixed.onnx")
print("✅ Saved reshaped-free model as yolov4-tiny-fixed.onnx")