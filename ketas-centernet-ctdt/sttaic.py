import tensorflow as tf

# Load dynamic saved_model
model = tf.saved_model.load("saved_model_dir")  # replace with your path
infer = model.signatures["serving_default"]

# Define static shape: [1, 512, 512, 3]
@tf.function(input_signature=[tf.TensorSpec(shape=[1, 512, 512, 3], dtype=tf.float32)])
def static_func(input_tensor):
    return infer(input_tensor)

# Save new static model
tf.saved_model.save(
    model,
    "saved_model_static",  # output path
    signatures=static_func.get_concrete_function(tf.TensorSpec([1, 512, 512, 3], tf.float32))
)