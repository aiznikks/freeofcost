import tensorflow as tf
import tf2onnx

# Load dynamic VIT model
model = tf.keras.models.load_model("vit.h5")

# Define static input signature
spec = (tf.TensorSpec((1, 384, 384, 3), tf.float32, name="input"),)

# Convert to ONNX with static input shape
model_proto, _ = tf2onnx.convert.from_keras(
    model,
    input_signature=spec,
    opset=13,
    output_path="vit_fp32.onnx"
)

print("Saved static ONNX: vit_fp32.onnx")