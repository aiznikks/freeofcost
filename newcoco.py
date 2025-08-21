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






second36272727step:

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