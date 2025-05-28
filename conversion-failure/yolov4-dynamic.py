import onnx

model = onnx.load("yolov4-tiny-single-batch.onnx")

# Make input and output batch size dynamic
model.graph.input[0].type.tensor_type.shape.dim[0].dim_param = 'batch'
model.graph.output[0].type.tensor_type.shape.dim[0].dim_param = 'batch'

onnx.save(model, "yolov4-tiny-dynamic.onnx")
print("✅ Patched and saved as yolov4-tiny-dynamic.onnx")