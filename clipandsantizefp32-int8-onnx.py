from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="yolov4_tiny.onnx",
    model_output="yolov4_tiny_int8_dynamic.onnx",
    weight_type=QuantType.QInt8
)

print("✅ Dynamic quantization done.")
