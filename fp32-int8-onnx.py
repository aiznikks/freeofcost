from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import numpy as np

class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data = [
            {"input.1": np.random.uniform(0, 1, size=(1, 3, 416, 416)).astype(np.float32)}
            for _ in range(100)
        ]
        self.iterator = iter(self.data)

    def get_next(self):
        return next(self.iterator, None)

quantize_static(
    model_input="yolov4_tiny.onnx",
    model_output="yolov4_tiny_int8.onnx",
    calibration_data_reader=DummyDataReader(),
    quant_format="QOperator",
    activation_type=QuantType.QUInt8,
    weight_type=QuantType.QInt8
)
