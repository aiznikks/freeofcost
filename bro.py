import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import CalibrationDataReader

class YOLOv4TinyDataReader(CalibrationDataReader):
    def __init__(self, image_dir):
        self.image_paths = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        self.index = 0

    def get_next(self):
        if self.index >= len(self.image_paths):
            return None

        img = Image.open(self.image_paths[self.index]).resize((416, 416))
        img = np.asarray(img).astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC to CHW
        img = np.expand_dims(img, axis=0)  # Add batch dim

        self.index += 1
        return {"000_net": img}