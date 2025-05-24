torch.onnx.export(
    model,
    dummy_input,
    "yolov4_tiny.onnx",
    input_names=["input.1"],
    output_names=["output"],
    opset_version=11
)
