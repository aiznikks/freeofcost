import onnx
from onnx import helper

# Load the dynamic ONNX model
model_path = "vit_dynamic.onnx"
model = onnx.load(model_path)

# Modify input shape
for input_tensor in model.graph.input:
    dims = input_tensor.type.tensor_type.shape.dim
    # Set batch size to 1 (instead of dynamic)
    dims[0].dim_value = 1

# Save new static ONNX model
static_model_path = "vit_static.onnx"
onnx.save(model, static_model_path)

print(f"Saved static ONNX model at: {static_model_path}")