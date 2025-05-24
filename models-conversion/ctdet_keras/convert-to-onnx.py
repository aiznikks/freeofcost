python3 -m tf2onnx.convert --saved-model centernet_saved_model --output centernet_fp32.onnx --opset 13

python3 -m tf2onnx.convert --saved-model centernet_saved_model --output centernet_fp32.onnx --opset 13 --large_model
