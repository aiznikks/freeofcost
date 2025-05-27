from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import numpy as np

# Dummy calibration data reader
class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data = iter([
            {"input": np.random.rand(1, 1, 32, 32).astype(np.float32)}
            for _ in range(100)
        ])

    def get_next(self):
        return next(self.data, None)

# Run quantization
quantize_static(
    model_input="fsrcnn_fp32.onnx",
    model_output="fsrcnn_int8.onnx",
    calibration_data_reader=DummyDataReader(),
    quant_format=QuantType.QInt8
)

print("✅ INT8 quantization complete. Output saved as fsrcnn_int8.onnx")