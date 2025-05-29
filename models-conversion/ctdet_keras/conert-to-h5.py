import tensorflow as tf

saved_model_dir = "saved_model_dir"  # ✅ this is your folder, not .pb file

loaded = tf.saved_model.load(saved_model_dir)
concrete_func = loaded.signatures["serving_default"]

print("🔷 Input:")
for key, val in concrete_func.structured_input_signature[1].items():
    print(f"  Name: {key}, Shape: {val.shape}, Dtype: {val.dtype}")

print("\n🔶 Output:")
for key, val in concrete_func.structured_outputs.items():
    print(f"  Name: {key}, Shape: {val.shape}, Dtype: {val.dtype}")