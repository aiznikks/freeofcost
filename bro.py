import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType

# 💡 STEP 1: Custom reader to preprocess COCO val images
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
                img = img.resize((416, 416))
                img = np.asarray(img).astype(np.float32) / 255.0
                img = np.transpose(img, (2, 0, 1))
                img = np.expand_dims(img, axis=0)
                self.index += 1
                return {"000_net": img}  # 🔁 Check this input name in Netron if needed
            except Exception as e:
                print(f"⚠️ Skipping corrupted image: {self.image_paths[self.index]}")
                self.index += 1
        return None

# 💡 STEP 2: Path to COCO val images
reader = YOLOv4TinyDataReader("/path/to/val2017")  # <-- REPLACE THIS with your real path

# 💡 STEP 3: Run Quantization
quantize_static(
    model_input="yolov4-tiny-final.onnx",
    model_output="yolov4-tiny-int8.onnx",
    calibration_data_reader=reader,
    quant_format=QuantType.QInt8
)

print("🎉 Done: yolov4-tiny-int8.onnx saved successfully!")