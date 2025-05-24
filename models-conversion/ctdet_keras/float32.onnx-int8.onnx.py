from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="centernet_fp32.onnx",
    model_output="centernet_int8.onnx",
    weight_type=QuantType.QInt8  # Use int8 weights
)

print("✅ INT8 model saved as: centernet_int8.onnx")
