import numpy as np
import tensorflow as tf

class DummyDataset(tf.keras.utils.Sequence):
    def __init__(self, num_samples=20, img_size=(128, 128)):
        self.num_samples = num_samples
        self.img_size = img_size

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        image = np.random.rand(*self.img_size, 1).astype(np.float32)
        mask = np.random.randint(0, 2, size=(*self.img_size, 1)).astype(np.float32)
        return image, mask

def get_dummy_data():
    train = DummyDataset(num_samples=30)
    val = DummyDataset(num_samples=10)
    return train, val
