import tensorflow as tf

# Load the converted TFLite model
interpreter = tf.lite.Interpreter(model_path="ssd_mobilenet_v1_weight_quant.tflite")
interpreter.allocate_tensors()

# Get input details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("🔷 Input Tensor(s):")
for i, inp in enumerate(input_details):
    print(f"  Input {i}:")
    print(f"    Name: {inp['name']}")
    print(f"    Shape: {inp['shape']}")
    print(f"    Dtype: {inp['dtype']}")

print("\n🔶 Output Tensor(s):")
for i, out in enumerate(output_details):
    print(f"  Output {i}:")
    print(f"    Name: {out['name']}")
    print(f"    Shape: {out['shape']}")
    print(f"    Dtype: {out['dtype']}")