import torch
from model import FSRCNN

# Step 1: Create model
model = FSRCNN(upscale_factor=4)

# Step 2: Load the pretrained weights
state_dict = torch.load("fsrcnn_X4.pth", map_location='cpu')

# Debug: Print a few key names and shapes
model_keys = list(model.state_dict().keys())
weight_keys = list(state_dict.keys())

print("Sample model keys:", model_keys[:5])
print("Sample weight keys:", weight_keys[:5])

# Check one known key match
if "first_part.0.weight" in model.state_dict() and "first_part.0.weight" in state_dict:
    print("Model shape:", model.state_dict()["first_part.0.weight"].shape)
    print("Weight shape:", state_dict["first_part.0.weight"].shape)

# Step 3: Load the weights (strict=False if shape mismatch persists)
model.load_state_dict(state_dict)  # or strict=False for bypassing errors

model.eval()

# Step 4: Export
dummy_input = torch.randn(1, 1, 32, 32)

torch.onnx.export(
    model,
    dummy_input,
    "fsrcnn_fp32.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=13
)

print("✅ Exported to fsrcnn_fp32.onnx")