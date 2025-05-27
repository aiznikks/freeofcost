import torch
from model import FSRCNN  # from model.py
import os

# Load model
model = FSRCNN(scale_factor=4)
model.load_state_dict(torch.load("fsrcnn_x4.pth", map_location='cpu'))  # Update if name differs
model.eval()

# Dummy input (grayscale input image: 1x1x32x32)
dummy_input = torch.randn(1, 1, 32, 32)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    "fsrcnn_fp32.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=13
)

print("Exported FSRCNN model to fsrcnn_fp32.onnx")