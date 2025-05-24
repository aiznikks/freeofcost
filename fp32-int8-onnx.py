from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
import numpy as np

class DummyDataReader(CalibrationDataReader):
    def get_next(self):
        for _ in range(100):
            yield {"input": np.random.rand(1, 3, 416, 416).astype(np.float32)}

quantize_static(
    model_input="yolov4_tiny.onnx",
    model_output="yolov4_tiny_int8.onnx",
    calibration_data_reader=DummyDataReader(),
    quant_format=QuantType.QOperator
)

print("✅ INT8 Quantized model saved: yolov4_tiny_int8.onnx")
