import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType

# 🧠 PLACE IT HERE — Custom Data Reader with Resize & Skip Protection
class YOLOv4TinyDataReader(CalibrationDataReader):
    def __init__(self, image_dir):
        self.image_paths = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        self.index = 0

    def get_next(self):
        while self.index < len(self.image_paths):
            try:
                img = Image.open(self.image_paths[self.index]).convert("RGB")
                img = img.resize((416, 416))  # Ensure exact size
                img = np.asarray(img).astype(np.float32) / 255.0
                img = np.transpose(img, (2, 0, 1))  # HWC → CHW
                img = np.expand_dims(img, axis=0)   # Add batch dim
                self.index += 1
                return {"000_net": img}  # Replace if your model input name is different
            except Exception as e:
                print(f"⚠️ Skipping corrupted image: {self.image_paths[self.index]}")
                self.index += 1
        return None

# 🔧 Create data reader from your folder
reader = YOLOv4TinyDataReader("image_dir")  # replace with your calibration images folder path

# 🚀 Run static quantization
quantize_static(
    model_input="yolov4-tiny-clean.onnx",
    model_output="yolov4-tiny-int8.onnx",
    calibration_data_reader=reader,
    quant_format=QuantType.QInt8
)

print("✅ INT8 Quantization Complete: yolov4-tiny-int8.onnx saved.")