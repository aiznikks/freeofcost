import onnx

model = onnx.load("yolov4_tiny.onnx")
input_all = [node.name for node in model.graph.input]
print("Input names:", input_all)
