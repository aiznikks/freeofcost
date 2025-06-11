interpreter = tf.lite.Interpreter(model_path="resnet_v2_50_fp32_static.tflite")
interpreter.allocate_tensors()

inputs = interpreter.get_input_details()
outputs = interpreter.get_output_details()

print("Inputs:", inputs)
print("Outputs:", outputs)