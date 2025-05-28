from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType

quantize_static(
    model_input="yolov4-tiny.onnx",
    model_output="yolov4-tiny-int8.onnx",
    calibration_data_reader=my_data_reader,
    quant_format=QuantType.QInt8
)