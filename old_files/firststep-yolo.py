import torch
from tool.darknet2pytorch import Darknet

# Load your model
model = Darknet("yolov4-tiny.cfg")
model.load_weights("yolov4_tiny.pth")
model.eval()

# Dummy input
dummy_input = torch.randn(1, 3, 416, 416)

# Re-export to ONNX with clean output names
torch.onnx.export(
    model,
    dummy_input,
    "yolov4_tiny_fixed.onnx",
    input_names=["input.1"],
    output_names=["boxes", "scores"],
    opset_version=11
)

print("✅ Exported yolov4_tiny_fixed.onnx with renamed outputs.")
