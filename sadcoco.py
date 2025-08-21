varify:Convert TF1 frozen graph → TFLite FP32

import tensorflow as tf
from tensorflow.python.platform import gfile

pb_path = "frozen_inference_graph.pb"  # inside the tarball
with tf.compat.v1.Session() as sess:
    with gfile.FastGFile(pb_path,'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    for op in tf.compat.v1.get_default_graph().get_operations():
        if op.name == 'image_tensor':
            print(op.outputs[0].shape)  # -> (1, ?, ?, 3)
            
            
            



step 2   Post-Training INT8 Quantization (full-int8 with calibration)

import tensorflow as tf

converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    graph_def_file="frozen_inference_graph.pb",
    input_arrays=["image_tensor"],
    output_arrays=[
        "TFLite_Detection_PostProcess",
        "TFLite_Detection_PostProcess:1",
        "TFLite_Detection_PostProcess:2",
        "TFLite_Detection_PostProcess:3",
    ],
    input_shapes={"image_tensor":[1,300,300,3]}
)
converter.allow_custom_ops = True         # needed for Detection_PostProcess
tflite_fp32 = converter.convert()
open("ssd_mobilenet_v1_coco_fp32.tflite","wb").write(tflite_fp32)





fulllint8
import numpy as np
import tensorflow as tf
from PIL import Image
import glob

def rep_data_gen():
    for path in glob.glob("repset/*.jpg")[:200]:
        img = Image.open(path).convert("RGB").resize((300,300))
        arr = np.array(img, dtype=np.uint8)         # uint8 is fine for SSD v1
        arr = arr.reshape(1,300,300,3)
        yield [arr]

converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    "frozen_inference_graph.pb",
    ["image_tensor"],
    ["TFLite_Detection_PostProcess",
     "TFLite_Detection_PostProcess:1",
     "TFLite_Detection_PostProcess:2",
     "TFLite_Detection_PostProcess:3"],
    input_shapes={"image_tensor":[1,300,300,3]}
)
converter.allow_custom_ops = True
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = rep_data_gen

# If your runtime prefers uint8 I/O:
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_int8 = converter.convert()
open("ssd_mobilenet_v1_coco_int8.tflite","wb").write(tflite_int8)
