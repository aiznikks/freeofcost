import onnx

model = onnx.load("vit_fp32.onnx")

# Fix output batch size
for output in model.graph.output:
    output.type.tensor_type.shape.dim[0].dim_value = 1  # Set batch=1

# Save fixed model
onnx.save(model, "vit_fp32_static.onnx")
print("Output shape fixed to [1, 1000]")