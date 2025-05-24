import torch
import argparse
import sys
sys.path.insert(0, '.')

from darknet2pytorch import Darknet

parser = argparse.ArgumentParser()
parser.add_argument('--weights', type=str, required=True)
parser.add_argument('--cfg', type=str, required=True)
parser.add_argument('--output', type=str, default='yolov4_tiny.onnx')
args = parser.parse_args()

model = Darknet(args.cfg)
model.load_weights(args.weights)
model.eval()

dummy_input = torch.randn(1, 3, model.height, model.width)
torch.onnx.export(
    model, 
    dummy_input, 
    args.output,
    verbose=False,
    opset_version=11
)

print(f"✅ ONNX model exported to {args.output}")
