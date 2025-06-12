import onnx

model = onnx.load("vit_fp32.onnx")

print("Inputs:")
for i in model.graph.input:
    print(i.name, [d.dim_value for d in i.type.tensor_type.shape.dim])

print("\nOutputs:")
for o in model.graph.output:
    print(o.name, [d.dim_value for d in o.type.tensor_type.shape.dim])