import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType

class YOLOv4TinyDataReader(CalibrationDataReader):
    def __init__(self, image_dir):
        self.image_paths = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        self.index = 0

    def get_next(self):
        if self.index >= len(self.image_paths):
            return None

        image = Image.open(self.image_paths[self.index]).resize((416, 416)).convert("RGB")
        image = np.asarray(image).astype(np.float32) / 255.0
        image = np.transpose(image, (2, 0, 1))  # HWC to CHW
        image = np.expand_dims(image, axis=0)   # Add batch dimension

        self.index += 1
        return {"000_net": image}

reader = YOLOv4TinyDataReader("image_dir")  # path to folder with 100 .jpg images

quantize_static(
    model_input="yolov4-tiny-dynamic.onnx",
    model_output="yolov4-tiny-int8.onnx",
    calibration_data_reader=reader,
    quant_format=QuantType.QInt8
)

print("✅ Quantized INT8 model saved as yolov4-tiny-int8.onnx")