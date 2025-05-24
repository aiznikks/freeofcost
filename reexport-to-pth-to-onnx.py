import torch
from tool.darknet2pytorch import Darknet

# Load the YOLOv4-Tiny model
model = Darknet("yolov4-tiny.cfg")
model.load_weights("yolov4_tiny.pth")
model.eval()

# Create dummy input for export
dummy_input = torch.randn(1, 3, 416, 416)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    "yolov4_tiny.onnx",
    input_names=["input.1"],
    output_names=["output"],
    opset_version=11
)

print("✅ Successfully exported yolov4_tiny.onnx")
