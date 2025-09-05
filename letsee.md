# TFLite Model Download & PTQ Guide (Office-safe, Mirror-aware)

*Last updated: 2025-09-05 (IST). Scope: download TFLite models in restricted networks, verify, and (if downloads fail) export FP32 → INT8 (signed) via static PTQ.*

---

## What you’ll get

* A **mirror-aware downloader** with proxy + allowlist support.
* A **TSV mirrors list** you can edit.
* A **verification script** using `benchmark_model`.
* A **strict FP32 → INT8 (S8)** TFLite PTQ snippet when downloads are blocked.
* A clean folder layout + logs + a “missing queue”.

---

## Prerequisites

```bash
# System tools
sudo apt-get update
sudo apt-get install -y curl unzip python3 python3-pip

# Python libs (used for optional export/PTQ)
python3 -m pip install --upgrade pip
python3 -m pip install tensorflow numpy pillow

# Optional: Kaggle CLI if you plan to add Kaggle sources to TSV
python3 -m pip install kaggle
# Setup credentials if you will use Kaggle CLI
# Place ~/.kaggle/kaggle.json with your API key (mode 600)
```

> Corporate proxy (optional):

```bash
export HTTPS_PROXY=http://proxy.company:8080
export HTTP_PROXY=http://proxy.company:8080
```

---

## Folder layout

```text
ptq/
  models/
    src_tflite/         # downloaded .tflite files (by family/model)
    logs/               # download + verify logs, missing list
  scripts/              # helper scripts
  data/                 # (optional) sample images for verification
```

Create it:

```bash
mkdir -p ptq/models/src_tflite ptq/models/logs ptq/scripts ptq/data
```

---

## 1) Mirror-aware downloader

Save as `ptq/scripts/mirror_fetch.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./mirror_fetch.sh tflite_mirrors.tsv ptq
#
# Env (optional):
#   HTTPS_PROXY / HTTP_PROXY
#   DOMAIN_ALLOWLIST="kaggle.com,storage.googleapis.com,download.tensorflow.org,raw.githubusercontent.com,huggingface.co,github.com,aihub.qualcomm.com"
#   CONNECT_TIMEOUT=10  MAX_TIME=600  RETRIES=3

TSV="${1:?mirrors tsv required}"
ROOT="${2:-ptq}"
OUT_DIR="$ROOT/models/src_tflite"
LOG_DIR="$ROOT/models/logs"
MISSED="$LOG_DIR/missing_tflite.txt"

mkdir -p "$OUT_DIR" "$LOG_DIR"
: > "$MISSED"

CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-10}"
MAX_TIME="${MAX_TIME:-600}"
RETRIES="${RETRIES:-3}"
DOMAIN_ALLOWLIST="${DOMAIN_ALLOWLIST:-}"

allow() {
  # If no allowlist set → allow all
  [[ -z "$DOMAIN_ALLOWLIST" ]] && return 0
  local host="$1"
  IFS=',' read -ra A <<< "$DOMAIN_ALLOWLIST"
  for d in "${A[@]}"; do
    [[ -n "$d" && "$host" == *"$d"* ]] && return 0
  done
  return 1
}

fetch_one(){
  local url="$1" dst="$2"
  local host
  host="$(echo "$url" | awk -F/ '{print $3}')"
  if ! allow "$host"; then
    echo "BLOCK (not in allowlist) $host -> $url"
    return 2
  fi
  echo "GET  $url"
  curl -fL --retry "$RETRIES" --retry-delay 2 \
       --connect-timeout "$CONNECT_TIMEOUT" --max-time "$MAX_TIME" \
       --continue-at - -o "$dst" "$url"
}

# TSV columns:
# family\tmodel\tfilename\tsha256\turl1\turl2\turl3...
# Lines starting with # are ignored.

while IFS=$'\t' read -r family model filename sha256 rest; do
  [[ -z "${family:-}" || "${family:0:1}" == "#" ]] && continue
  outdir="$OUT_DIR/$family/$model"
  mkdir -p "$outdir"
  dst="$outdir/$filename"

  ok=0
  urls=()
  IFS=$'\t' read -r -a fields <<< "$rest"
  for u in "${fields[@]}"; do
    [[ -n "$u" ]] && urls+=("$u")
  done

  for u in "${urls[@]}"; do
    if fetch_one "$u" "$dst"; then
      if [[ -n "$sha256" ]]; then
        got="$(sha256sum "$dst" | awk '{print $1}')"
        if [[ "$got" != "$sha256" ]]; then
          echo "SHA256 mismatch for $model ($got != $sha256). Trying next mirror."
          rm -f "$dst"
          continue
        fi
      fi
      echo "OK   $family/$model -> $filename"
      ok=1
      break
    fi
  done

  if [[ $ok -eq 0 ]]; then
    echo "FAIL $family/$model -> $filename" | tee -a "$MISSED"
  fi
done < "$TSV"

echo
if [[ -s "$MISSED" ]]; then
  echo "Some models missing. See $MISSED"
else
  echo "All requested TFLite items downloaded."
fi
```

Make it executable:

```bash
chmod +x ptq/scripts/mirror_fetch.sh
```

---

## 2) Mirrors list (TSV)

Save as `ptq/scripts/tflite_mirrors.tsv` (tab-separated).
Columns: `family  model  filename  sha256  url1  url2  url3`

```tsv
# family	model	filename	sha256	url1	url2	url3
# --- Classification ---
classification	inception_v3	inception_v3.tflite		https://storage.googleapis.com/download.tensorflow.org/models/tflite/gpu/inception_v3_2018_04_27.tflite	https://raw.githubusercontent.com/tensorflow/models/master/research/lstm_object_detection/sample_data/inception_v3_2016_08_28_frozen.tflite	
classification	mobilenet_v1_1.0_224	mobilenet_v1_1.0_224_quant.tflite		https://storage.googleapis.com/mobilenet_v1/mobilenet_v1_1.0_224_quant.tflite	https://raw.githubusercontent.com/PINTO0309/PINTO_model_zoo/main/001_MobileNetV1/resources/mobilenet_v1_1.0_224_quant.tflite	
classification	mobilenet_v2_1.0_224	mobilenet_v2_1.0_224.tflite		https://storage.googleapis.com/mobilenet_v2/checkpoints/mobilenet_v2_1.0_224.tflite	https://raw.githubusercontent.com/PINTO0309/PINTO_model_zoo/main/004_MobileNetV2/resources/mobilenet_v2_1.0_224.tflite	
# ResNet50 v1/v2: no stable official CPU .tflite → convert yourself

# --- Object Detection ---
detection	ssd_mobilenet_v1	ssd_mobilenet_v1.tflite		https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip	https://raw.githubusercontent.com/PINTO0309/PINTO_model_zoo/main/022_SSD-MobileNet/ssd_mobilenet_v1.tflite	
# YOLOv3/YOLOv4-Tiny: community .tflite varies per region; add your trusted mirror if allowed

# --- Pose Estimation ---
pose	posenet_multipose_mnet_v1	posenet_mobilenet_v1_075_481_641_quant_decoder.tflite		https://raw.githubusercontent.com/google-coral/project-posenet/master/models/posenet_mobilenet_v1_075_481_641_quant_decoder.tflite	https://raw.githubusercontent.com/google-coral/project-posenet/master/models/posenet_mobilenet_v1_100_353_481_quant_decoder.tflite	

# --- Segmentation ---
segmentation	deeplabv3plus	deeplabv3_mnv2_dm05_pascal.tflite		https://storage.googleapis.com/download.tensorflow.org/models/tflite/deeplabv3_mnv2_dm05_pascal_quant.tflite		
segmentation	unet	Unet-Segmentation.tflite		https://huggingface.co/qualcomm/Unet-Segmentation/resolve/7d15931279d52728d718e5e2b4f71b01e8650be0/Unet-Segmentation.tflite?download=true	https://raw.githubusercontent.com/PINTO0309/TensorflowLite-UNet/master/models/Unet-Segmentation.tflite	

# --- Super Resolution ---
# EDSR / FSRCNN: typically convert yourself; add mirrors if your org approves
```

> Optional strict allowlist (recommended in enterprises):

```bash
export DOMAIN_ALLOWLIST="storage.googleapis.com,download.tensorflow.org,raw.githubusercontent.com,huggingface.co,github.com,aihub.qualcomm.com"
```

---

## 3) Run the downloads

```bash
# Optional proxy + allowlist
export HTTPS_PROXY=http://proxy.company:8080
export HTTP_PROXY=http://proxy.company:8080
export DOMAIN_ALLOWLIST="storage.googleapis.com,download.tensorflow.org,raw.githubusercontent.com,huggingface.co,github.com,aihub.qualcomm.com"

# Fetch
ptq/scripts/mirror_fetch.sh ptq/scripts/tflite_mirrors.tsv ptq
```

Outputs:

* Files in `ptq/models/src_tflite/<family>/<model>/*.tflite`
* Log in `ptq/models/logs/download.log` (captured by your shell)
* Missing list in `ptq/models/logs/missing_tflite.txt`

---

## 4) Verify TFLite files on x86

Save as `ptq/scripts/verify_tflite.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-ptq}"
OUT="$ROOT/models/src_tflite"
LOG_DIR="$ROOT/models/logs"
CSV="$LOG_DIR/verify_tflite.csv"
: > "$CSV"

# Ensure benchmark_model is in PATH (from TFLite or Android NNAPI host tools)
cmd="${BENCHMARK_MODEL_BIN:-benchmark_model}"

echo "file,ok,avg_ms,notes" >> "$CSV"

while IFS= read -r -d '' f; do
  name="$(basename "$f")"
  echo "Verify $name"
  if $cmd --graph="$f" --num_runs=50 --warmup_runs=5 --num_threads=4 >/tmp/bm.log 2>&1; then
    ms="$(grep -Eo 'median=\s*[0-9.]+' /tmp/bm.log | awk -F= '{print $2}' | xargs)"
    echo "$f,OK,$ms," >> "$CSV"
  else
    note="$(tail -n 2 /tmp/bm.log | tr ',' ';' | tr '\n' ' ')"
    echo "$f,FAIL,,${note}" >> "$CSV"
  fi
done < <(find "$OUT" -type f -name "*.tflite" -print0)

echo "CSV -> $CSV"
```

Make it executable and run:

```bash
chmod +x ptq/scripts/verify_tflite.sh
ptq/scripts/verify_tflite.sh ptq
```

Result CSV: `ptq/models/logs/verify_tflite.csv`

---

## 5) If downloads are blocked: export FP32 → TFLite → INT8 (S8 PTQ)

### 5.1 Export FP32 TFLite (example: MobileNetV2)

```bash
python3 - <<'PY'
import tensorflow as tf
import numpy as np

# FP32 Keras model (internet may be required to fetch weights)
m = tf.keras.applications.MobileNetV2(weights='imagenet')
tf.saved_model.save(m, "ptq/tmp/mnetv2_savedmodel")

conv = tf.lite.TFLiteConverter.from_saved_model("ptq/tmp/mnetv2_savedmodel")
tfl = conv.convert()
open("ptq/models/src_tflite/classification/mobilenet_v2_1.0_224/mobilenet_v2_1.0_224_float.tflite","wb").write(tfl)
print("Wrote float TFLite.")
PY
```

### 5.2 Strict **INT8 (signed) static PTQ** TFLite

> Representative dataset: small calibration set (50–500 samples). Place sample images under `ptq/data/cls_224/`.

```bash
python3 - <<'PY'
import os, glob
import numpy as np
import tensorflow as tf
from PIL import Image

SAVED="ptq/tmp/mnetv2_savedmodel"
OUT="ptq/models/src_tflite/classification/mobilenet_v2_1.0_224/mobilenet_v2_1.0_224_int8.tflite"
CAL_DIR="ptq/data/cls_224"

def rep_data():
    files = sorted(glob.glob(os.path.join(CAL_DIR, "*")))
    for p in files[:200]:
        img = Image.open(p).convert("RGB").resize((224,224))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = (arr - 0.5) / 0.5
        arr = np.expand_dims(arr, 0).astype(np.float32)
        yield [arr]

converter = tf.lite.TFLiteConverter.from_saved_model(SAVED)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = rep_data
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Enforce signed INT8 IO if your runtime requires true int8 pipeline
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tfl_int8 = converter.convert()
open(OUT, "wb").write(tfl_int8)
print("Wrote INT8 TFLite:", OUT)
PY
```

> This enforces **static PTQ** and **INT8 (S8)**.
> If an op forces float fallback, you’ll see increased size or errors; adjust model or use different source.

---

## 6) Compliance & safety checklist

* Use **official** or **well-known** sources.
* Keep **LICENSE/NOTICE** files with models.
* Respect **corporate proxy**; don’t bypass policy.
* Keep **download logs** and **checksums** when provided.
* Avoid unknown file-sharing sites.

---

## 7) Troubleshooting

* **403/blocked:** add the host to `DOMAIN_ALLOWLIST`.
* **Slow/timeout:** raise `CONNECT_TIMEOUT`, `MAX_TIME`, `RETRIES`.
* **Zip payloads:** some sources ship zips; add an unzip step if you put such URLs in TSV.
* **Benchmark tool missing:** set `BENCHMARK_MODEL_BIN=/path/to/benchmark_model`.
* **INT8 not enforced:** ensure `inference_input_type=int8` and `inference_output_type=int8`; verify with `benchmark_model` logs.

---

## 8) Quick commands (recap)

```bash
# 1) Download
export DOMAIN_ALLOWLIST="storage.googleapis.com,download.tensorflow.org,raw.githubusercontent.com,huggingface.co,github.com,aihub.qualcomm.com"
ptq/scripts/mirror_fetch.sh ptq/scripts/tflite_mirrors.tsv ptq

# 2) Verify
ptq/scripts/verify_tflite.sh ptq

# 3) If missing -> export FP32 then PTQ INT8 (example shown above)
```

---

If you want, I can also add a tiny **manifest generator** that hashes each `.tflite` and writes `ptq/models/logs/manifest.json` for your manager’s report.
