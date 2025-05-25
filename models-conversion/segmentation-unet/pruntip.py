import tensorflow as tf

model = tf.saved_model.load("unet_saved_model_fixed")
concrete_func = model.signatures["serving_default"]

for key, tensor in concrete_func.structured_input_signature[1].items():
    print(f"Input name: {key}, shape: {tensor.shape}, dtype: {tensor.dtype}")
