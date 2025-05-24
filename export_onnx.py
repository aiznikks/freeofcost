from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import numpy as np
import os

class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data_iter = iter([
            {"input": np.random.rand(1, 3, 416, 416).astype(np.float32)}
            for _ in range(100)
        ])

    def get_next(self):
        return next(self.data_iter, None)

# Run static quantization
quantize_static(
    model_input="yolov4_tiny.onnx",
    model_output="yolov4_tiny_int8.onnx",
    calibration_data_reader=DummyDataReader(),
    quant_format=QuantType.QInt8
)
