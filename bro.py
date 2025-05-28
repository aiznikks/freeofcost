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
                return {"000_net": img}
            except Exception as e:
                print(f"⚠️ Skipping corrupted image: {self.image_paths[self.index]}")
                self.index += 1
        return None