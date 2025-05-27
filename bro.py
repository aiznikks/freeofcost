from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import numpy as np
import os

# Dummy Data Reader for Calibration
class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data = iter([
            {"input": np.random.rand(1, 3, 64, 64).astype(np.float32)}
            for _ in range(100)  # 100 samples for calibration
        ])

    def get_next(self):
        return next(self.data, None)

# Quantize the model
quantize_static(
    model_input="edsr_fp32.onnx",
    model_output="edsr_int8.onnx",
    calibration_data_reader=DummyDataReader(),
    quant_format=QuantType.QInt8
)

print("Quantization complete. INT8 model saved as edsr_int8.onnx")