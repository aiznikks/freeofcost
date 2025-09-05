Here you go — a clean, copy-pasteable **Markdown** you can drop into your GitHub repo.
It lists **TFLite download sources** for each model you gave me (with **2–3 alternatives** where possible).
I’ve clearly flagged models that don’t have trusted, ready-made TFLite files so you can plan conversions.

---

# TFLite Download Map (FP32→INT8 PTQ Pipeline Prep)

*Last updated: 2025-09-05 (IST). Focus: x86; ARM64 later.*

> Use these links to fetch **plain TFLite** starting points (float or existing int8).
> For strict **FP32→INT8 (S8)** PTQ, re-export and quantize yourself when the binary is already quantized or lacks metadata.

---

## ✅ Classification

### ResNet-50 (v1)

* No official TensorFlow-hosted **TFLite** binary. Use TF/Keras or PyTorch and convert to TFLite yourself.

  * Keras API (for FP32 source → convert): [https://www.tensorflow.org/api\_docs/python/tf/keras/applications/ResNet50](https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50) ([TensorFlow][1])

### ResNet-50 v2

* Same situation as v1. Convert from TF/Keras saved model:

  * Keras applications index: [https://www.tensorflow.org/api\_docs/python/tf/keras/applications/](https://www.tensorflow.org/api_docs/python/tf/keras/applications/) (navigate to ResNet50V2) ([TensorFlow][1])

### Inception v3

* Kaggle Models (TensorFlow Hub mirror; **TFLite**): [https://www.kaggle.com/models/tensorflow/inception/tfLite/v3-metadata/1](https://www.kaggle.com/models/tensorflow/inception/tfLite/v3-metadata/1) ([Kaggle][2])
* TF blog page (has **download** reference): [https://blog.tensorflow.org/2020/04/tensorflow-lite-core-ml-delegate-faster-inference-iphones-ipads.html](https://blog.tensorflow.org/2020/04/tensorflow-lite-core-ml-delegate-faster-inference-iphones-ipads.html) ([blog.tensorflow.org][3])
* Qualcomm AI Hub model page (provides TFLite export path): [https://aihub.qualcomm.com/models/inception\_v3](https://aihub.qualcomm.com/models/inception_v3) ([Qualcomm AI Hub][4])

### MobileNet v1 (1.0, 224)

* Kaggle Models (**quantized TFLite** + metadata):

  * 1.0\_224: [https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/1-0-224-quantized-metadata/1?tfhub-redirect=true](https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/1-0-224-quantized-metadata/1?tfhub-redirect=true) ([Kaggle][5])
  * 0.25\_224 variant example: [https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/0-25-224-quantized-metadata/1?tfhub-redirect=true](https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/0-25-224-quantized-metadata/1?tfhub-redirect=true) ([Kaggle][6])
* TF blog (direct MobileNet v1 TFLite **download** reference): [https://blog.tensorflow.org/2019/01/tensorflow-lite-now-faster-with-mobile.html](https://blog.tensorflow.org/2019/01/tensorflow-lite-now-faster-with-mobile.html) ([blog.tensorflow.org][7])

### MobileNet v2 (1.0, 224)

* Kaggle Models (**float & quant** TFLite variants): [https://www.kaggle.com/models/tensorflow/mobilenet-v2](https://www.kaggle.com/models/tensorflow/mobilenet-v2) ([Kaggle][8])

### EfficientNet EdgeTPU-S

* Designed for EdgeTPU; plain CPU TFLite binaries are not typically hosted for this exact “EdgeTPU-S” variant. Use TF SavedModel → export to TFLite, or use Coral model pages when acceptable:

  * Coral model index (object detection/classification families; includes TFLite downloads): [https://coral.ai/models/object-detection/](https://coral.ai/models/object-detection/) ([Coral][9])

### ViT-B/16

* No official TFLite. Export from TF/PyTorch yourself (use ONNX/TF and convert).

  * Use TF/Keras or TorchVision ViT and then TFLite converter.

---

## ✅ Object Detection

### SSD MobileNet v1

* Kaggle Models (**TFLite**): [https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1/tfLite/default/1](https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1/tfLite/default/1) ([Kaggle][10])
* Model card root: [https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1](https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1) ([Kaggle][11])

### YOLOv3-Tiny

* No official TensorFlow TFLite binary; use community builds or convert from Darknet.

  * PINTO Model Zoo (multi-framework dumps incl. TFLite): [https://github.com/PINTO0309/PINTO\_model\_zoo](https://github.com/PINTO0309/PINTO_model_zoo) ([GitHub][12])
  * ModelZoo page (tutorial + artifacts): [https://www.modelzoo.co/model/tensorflow-yolov4-tflite](https://www.modelzoo.co/model/tensorflow-yolov4-tflite) (often covers YOLOv3/4 tiny pipelines as well) ([Model Zoo][13])

### YOLOv4-Tiny

* Community conversions/tutorials (TFLite):

  * ModelZoo (TensorFlow YOLOv4/Tiny to TFLite): [https://www.modelzoo.co/model/tensorflow-yolov4-tflite](https://www.modelzoo.co/model/tensorflow-yolov4-tflite) ([Model Zoo][13])
  * Context in PINTO issues (INT8 on RPi): [https://github.com/PINTO0309/PINTO\_model\_zoo/issues/44](https://github.com/PINTO0309/PINTO_model_zoo/issues/44) ([GitHub][14])

### DETR (ResNet-50)

* No stable/public **TFLite** binary due to op support. Keep this model in ONNX for now.

### CenterNet (ctdet)

* No official TFLite binary; most public artifacts are ONNX/TensorRT. Convert yourself if TFLite is mandatory.

---

## ✅ Pose Estimation

### Multi-person PoseNet (multi\_person\_mobilenet\_v1)

* Google Coral PoseNet (repo with TFLite models & scripts): [https://github.com/google-coral/project-posenet](https://github.com/google-coral/project-posenet) ([GitHub][15])
* Community Q\&A confirming multi-person TFLite availability: [https://stackoverflow.com/questions/68170600/does-tflite-version-of-posenet-model-support-multiple-pose-estimation](https://stackoverflow.com/questions/68170600/does-tflite-version-of-posenet-model-support-multiple-pose-estimation) ([Stack Overflow][16])
* Qualcomm Posenet-Mobilenet (deploy notes/TFLite export): [https://huggingface.co/qualcomm/Posenet-Mobilenet](https://huggingface.co/qualcomm/Posenet-Mobilenet) ([Hugging Face][17])

### CPN (Cascaded Pyramid Network)

* No widely trusted public TFLite binary. Convert from TF/PyTorch.

---

## ✅ Segmentation

### DeepLabV3+

* Kaggle Models (**TFLite**): [https://www.kaggle.com/models/tensorflow/deeplabv3/tfLite/metadata/1?tfhub-redirect=true](https://www.kaggle.com/models/tensorflow/deeplabv3/tfLite/metadata/1?tfhub-redirect=true) ([Kaggle][18])
* MathWorks example (automated download of Kaggle DeepLabV3 TFLite): [https://www.mathworks.com/help/coder/ug/generate-code-for-semantic-segmantation-using-tflite.html](https://www.mathworks.com/help/coder/ug/generate-code-for-semantic-segmantation-using-tflite.html) (see “Download Model”) ([MathWorks][19])
* Qualcomm AI Hub variant (TFLite export path): [https://huggingface.co/qualcomm/DeepLabV3-Plus-MobileNet](https://huggingface.co/qualcomm/DeepLabV3-Plus-MobileNet) ([Hugging Face][20])

### U-Net

* Qualcomm AI Hub (direct **Unet-Segmentation.tflite**):

  * File: [https://huggingface.co/qualcomm/Unet-Segmentation/blob/7d15931279d52728d718e5e2b4f71b01e8650be0/Unet-Segmentation.tflite](https://huggingface.co/qualcomm/Unet-Segmentation/blob/7d15931279d52728d718e5e2b4f71b01e8650be0/Unet-Segmentation.tflite) ([Hugging Face][21])
  * Model page: [https://aihub.qualcomm.com/models/unet\_segmentation](https://aihub.qualcomm.com/models/unet_segmentation) ([Qualcomm AI Hub][22])
* Community implementation (TFLite U-Net): [https://github.com/PINTO0309/TensorflowLite-UNet](https://github.com/PINTO0309/TensorflowLite-UNet) ([GitHub][23])

---

## ✅ Super-Resolution

### EDSR

* Community repo with TFLite EDSR artifacts/notebooks: [https://github.com/freedomtan/some\_super\_resolution\_tflite\_models](https://github.com/freedomtan/some_super_resolution_tflite_models) ([GitHub][24])
* (If you prefer to train/convert) TF impl to export: [https://github.com/Saafke/EDSR\_Tensorflow](https://github.com/Saafke/EDSR_Tensorflow) ([GitHub][25])

### FSRCNN

* Community TF/TFLite implementations are common; export yourself from TF and convert.

---

## ✅ Face Detection (Face\_MobileNetV1\_SSD)

* Use **SSD MobileNet v1** TFLite as the base face detector (trained on face datasets in many repos).

  * Kaggle Models (general SSD MobileNet v1 TFLite): [https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1](https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1) ([Kaggle][11])
* MediaPipe Face Detector (task page; modern alternative, non-SSD): [https://ai.google.dev/edge/mediapipe/solutions/vision/face\_detector](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector) ([Google AI for Developers][26])

---

## Notes

* **Kaggle Models** hosts many TensorFlow Hub TFLite binaries with metadata; prefer these where available. ([Kaggle][8])
* **Community sources** (PINTO Model Zoo, ModelZoo.co, various GitHubs) provide TFLite builds for YOLO/UNet/EDSR etc. Validate with `benchmark_model` before relying on them. ([GitHub][12], [Model Zoo][13])
* If a model has **no official TFLite**, your safest route is: FP32 SavedModel (or PyTorch) → export TF SavedModel → TFLite Converter → PTQ.

---

### Quick sanity check before PTQ

* Ensure the file is **plain TFLite** (float or quantized).
* If it’s already **INT8**, you may still need to **re-export** from FP32 to meet the “FP32→INT8 (S8)” mandate.
* Run on x86 with LiteRT `benchmark_model` to confirm load and input tensor shapes.

---

If you want, I can generate a tiny shell script that **wget/curl**-downloads the above into `ptq/models/src_tflite/` with the same folder names you’re using, so Cursor can pick them up automatically.

[1]: https://www.tensorflow.org/api_docs/python/tf/keras/applications/InceptionV3?utm_source=chatgpt.com "tf.keras.applications.InceptionV3 | TensorFlow v2.16.1"
[2]: https://www.kaggle.com/models/tensorflow/inception/tfLite/v3-metadata/1?utm_source=chatgpt.com "TensorFlow | inception"
[3]: https://blog.tensorflow.org/2020/04/tensorflow-lite-core-ml-delegate-faster-inference-iphones-ipads.html?utm_source=chatgpt.com "TensorFlow Lite Core ML delegate enables faster ..."
[4]: https://aihub.qualcomm.com/models/inception_v3?utm_source=chatgpt.com "Inception-v3"
[5]: https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/1-0-224-quantized-metadata/1?tfhub-redirect=true&utm_source=chatgpt.com "TensorFlow | mobilenet_v1"
[6]: https://www.kaggle.com/models/tensorflow/mobilenet-v1/tfLite/0-25-224-quantized-metadata/1?tfhub-redirect=true&utm_source=chatgpt.com "TensorFlow | mobilenet_v1"
[7]: https://blog.tensorflow.org/2019/01/tensorflow-lite-now-faster-with-mobile.html?utm_source=chatgpt.com "TensorFlow Lite Now Faster with Mobile GPUs"
[8]: https://www.kaggle.com/models/tensorflow/mobilenet-v2?utm_source=chatgpt.com "TensorFlow | mobilenet_v2"
[9]: https://coral.ai/models/object-detection/?utm_source=chatgpt.com "Models - Object Detection - Coral"
[10]: https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1/tfLite/default/1?utm_source=chatgpt.com "TensorFlow | ssd_mobilenet_v1"
[11]: https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1?utm_source=chatgpt.com "TensorFlow | ssd_mobilenet_v1"
[12]: https://github.com/PINTO0309/PINTO_model_zoo?utm_source=chatgpt.com "PINTO0309/PINTO_model_zoo"
[13]: https://www.modelzoo.co/model/tensorflow-yolov4-tflite?utm_source=chatgpt.com "tensorflow yolov4 tflite"
[14]: https://github.com/PINTO0309/PINTO_model_zoo/issues/44?utm_source=chatgpt.com "yolov4-tiny with RaspberryPi · Issue #44"
[15]: https://github.com/google-coral/project-posenet?utm_source=chatgpt.com "google-coral/project-posenet: Human Pose Detection on ..."
[16]: https://stackoverflow.com/questions/68170600/does-tflite-version-of-posenet-model-support-multiple-pose-estimation?utm_source=chatgpt.com "Does tflite version of poseNet model support multiple pose ..."
[17]: https://huggingface.co/qualcomm/Posenet-Mobilenet?utm_source=chatgpt.com "qualcomm/Posenet-Mobilenet · Hugging Face"
[18]: https://www.kaggle.com/models/tensorflow/deeplabv3/tfLite/metadata/1?tfhub-redirect=true&utm_source=chatgpt.com "deeplabv3 - TensorFlow"
[19]: https://www.mathworks.com/help/coder/ug/generate-code-for-semantic-segmantation-using-tflite.html?utm_source=chatgpt.com "Deploy Semantic Segmentation Application Using ..."
[20]: https://huggingface.co/qualcomm/DeepLabV3-Plus-MobileNet?utm_source=chatgpt.com "qualcomm/DeepLabV3-Plus-MobileNet"
[21]: https://huggingface.co/qualcomm/Unet-Segmentation/blob/7d15931279d52728d718e5e2b4f71b01e8650be0/Unet-Segmentation.tflite?utm_source=chatgpt.com "Unet-Segmentation.tflite · qualcomm/ ..."
[22]: https://aihub.qualcomm.com/models/unet_segmentation?utm_source=chatgpt.com "Unet-Segmentation"
[23]: https://github.com/PINTO0309/TensorflowLite-UNet?utm_source=chatgpt.com "PINTO0309/TensorflowLite-UNet"
[24]: https://github.com/freedomtan/some_super_resolution_tflite_models?utm_source=chatgpt.com "Some super resolutions models converted to TFLite"
[25]: https://github.com/Saafke/EDSR_Tensorflow?utm_source=chatgpt.com "Saafke/EDSR_Tensorflow: TensorFlow implementation of ' ..."
[26]: https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector?utm_source=chatgpt.com "Face detection guide | Google AI Edge - Gemini API"
