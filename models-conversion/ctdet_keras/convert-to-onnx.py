import tf2onnx
import tensorflow as tf

# Path to your saved model
saved_model_dir = "centernet_saved_model"

# Convert
model_proto, _ = tf2onnx.convert.from_saved_model(
    saved_model_dir,
    output_path="centernet_fp32.onnx",
    opset=13
)

print("✅ Exported float32 ONNX model: centernet_fp32.onnx")
