import tensorflow as tf

# === Step 1: Load existing SavedModel ===
original_model_dir = "path/to/saved_model_dir"
loaded_model = tf.saved_model.load(original_model_dir)

# === Step 2: Define static shape input wrapper ===
@tf.function(input_signature=[tf.TensorSpec([1, 512, 512, 3], dtype=tf.float32)])
def static_input_fn(x):
    return loaded_model(x)

concrete_func = static_input_fn.get_concrete_function()

# === Step 3: Save new SavedModel with static shape ===
static_model_dir = "deeplabv3p_static_saved_model"
tf.saved_model.save(loaded_model, static_model_dir, signatures=concrete_func)

# === Step 4: Convert to static FP32 TFLite ===
converter = tf.lite.TFLiteConverter.from_saved_model(static_model_dir)
converter.optimizations = []
converter.inference_input_type = tf.float32
converter.inference_output_type = tf.float32

tflite_model = converter.convert()

# === Step 5: Save TFLite file ===
with open("deeplabv3p_fp32_static.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite conversion complete. Output: deeplabv3p_fp32_static.tflite")