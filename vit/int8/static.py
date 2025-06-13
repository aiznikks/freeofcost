from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import onnx
import numpy as np

class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        self.data = {"input": np.random.rand(1, 3, 224, 224).astype(np.float32)}
        self.enum_data = None

    def get_next(self):
        if not self.enum_data:
            self.enum_data = iter([self.data])
        return next(self.enum_data, None)

# Load original dynamic FP32 ONNX model
model_fp32 = "vit_fp32.onnx"
model_int8 = "vit_int8_static.onnx"

# Perform static quantization
quantize_static(
    model_input=model_fp32,
    model_output=model_int8,
    calibration_data_reader=DummyDataReader(),
    quant_format=QuantType.QOperator,
    per_channel=False
)

print("Quantization complete. Static INT8 ONNX saved at:", model_int8)