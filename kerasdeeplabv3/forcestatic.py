import tensorflow as tf
from tensorflow import keras

# Load original model (you can load from .h5 or build it directly)
model = tf.keras.models.load_model("path/to/deeplabv3p_model")

# Set static input shape here
@tf.function(input_signature=[tf.TensorSpec(shape=[1, 512, 512, 3], dtype=tf.float32)])
def static_model(input_tensor):
    return model(input_tensor)

# Save as new static SavedModel
tf.saved_model.save(model, "deeplabv3p_static_saved_model", signatures=static_model.get_concrete_function())