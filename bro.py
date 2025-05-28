import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType

# Step 1: Define the Calibration Data Reader
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
        image = np.transpose(image, (2, 0, 1))  # HWC → CHW
        image = np.expand_dims(image, axis=0)   # Add batch dim → (1, 3, 416, 416)

        self.index += 1
        return {"000_net": image}  # Replace "000_net" if your input name is different

# Step 2: Create the calibration reader
reader = YOLOv4TinyDataReader("image_dir")  # replace with your image folder path

# Step 3: Run quantization
quantize_static(
    model_input="yolov4-tiny-clean.onnx",
    model_output="yolov4-tiny-int8.onnx",
    calibration_data_reader=reader,
    quant_format=QuantType.QInt8
)

print("✅ INT8 Quantization Complete: yolov4-tiny-int8.onnx generated")