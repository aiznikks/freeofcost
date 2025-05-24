import keras2onnx
from tensorflow.keras.models import load_model
import onnx

# Load Keras H5 model
model = load_model("centernet_model.h5", compile=False)

# Convert to ONNX
onnx_model = keras2onnx.convert_keras(model, model.name)

# Save ONNX model
onnx.save_model(onnx_model, "centernet_fp32.onnx")

print("✅ ONNX model saved as centernet_fp32.onnx")
