from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
from PIL import Image
import numpy as np

class DummyDataReader(CalibrationDataReader):
    def __init__(self):
        image = Image.open("data/dog.jpg").resize((416, 416)).convert("RGB")
        arr = np.asarray(image).astype(np.float32) / 255.0

        # Clip and sanitize
        arr = np.clip(arr, 0.001, 1.0)  # avoid exact zeros
        arr += 1e-6                     # force scale to be non-zero

        arr = arr.transpose(2, 0, 1).reshape(1, 3, 416, 416)
        self.data = [{"input.1": arr} for _ in range(100)]
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
