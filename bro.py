import onnx

model = onnx.load("yolov4-tiny-single-batch.onnx")

print("🔍 Reshape Nodes:")
for node in model.graph.node:
    if node.op_type == "Reshape":
        print(f"Name: {node.name}")
        print(f"Inputs: {node.input}")
        print(f"Outputs: {node.output}")
        print("-" * 40)