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

    def get_input_shape(self):
        return (self.img_size[0], self.img_size[1], 1)

    def get_output_shape(self):
        return (self.img_size[0], self.img_size[1], 1)
        
        
        
        
        #convert-saved-model
        import tensorflow as tf

model = tf.keras.models.load_model("unet_dummy.h5", compile=False)
tf.saved_model.save(model, "unet_saved_model")
        