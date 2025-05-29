import os
import cv2
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# === UPDATE THESE IF YOUR STRUCTURE IS DIFFERENT ===
ANNOTATION_FILE = "wider_face_split/wider_face_train_bbx_gt.txt"
IMAGE_DIR = "WIDER_train/images"
OUTPUT_DIR = "annotations_xml"
# ===================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_xml(image_path, image_rel_path, bboxes):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"⚠️ Unreadable image: {image_rel_path}")
            return
        height, width, depth = img.shape
    except Exception as e:
        print(f"❌ Failed to read {image_rel_path}: {e}")
        return

    annotation = Element('annotation')
    SubElement(annotation, 'folder').text = os.path.basename(os.path.dirname(image_rel_path))
    SubElement(annotation, 'filename').text = image_rel_path
    SubElement(annotation, 'path').text = os.path.abspath(image_path)

    size = SubElement(annotation, 'size')
    SubElement(size, 'width').text = str(width)
    SubElement(size, 'height').text = str(height)
    SubElement(size, 'depth').text = str(depth)

    for bbox in bboxes:
        x, y, w, h = bbox
        if w <= 0 or h <= 0:
            continue

        obj = SubElement(annotation, 'object')
        SubElement(obj, 'name').text = 'face'
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'

        bndbox = SubElement(obj, 'bndbox')
        SubElement(bndbox, 'xmin').text = str(int(x))
        SubElement(bndbox, 'ymin').text = str(int(y))
        SubElement(bndbox, 'xmax').text = str(int(x + w))
        SubElement(bndbox, 'ymax').text = str(int(y + h))

    rough_string = tostring(annotation, 'utf-8')
    reparsed = parseString(rough_string)
    out_file = os.path.join(OUTPUT_DIR, image_rel_path.replace('/', '_').replace('.jpg', '.xml'))

    with open(out_file, 'w') as f:
        f.write(reparsed.toprettyxml(indent="  "))

def parse_annotations():
    if not os.path.exists(ANNOTATION_FILE):
        print(f"❌ Error: Annotation file not found at {ANNOTATION_FILE}")
        return

    with open(ANNOTATION_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    total = len(lines)
    while i < total:
        image_rel_path = lines[i]
        image_path = os.path.join(IMAGE_DIR, image_rel_path)
        i += 1

        if i >= total:
            break

        try:
            face_count = int(lines[i])
        except:
            print(f"⚠️ Malformed count for {image_rel_path}")
            i += 1
            continue
        i += 1

        bboxes = []
        for _ in range(face_count):
            if i >= total:
                break
            parts = lines[i].split()
            if len(parts) >= 4:
                try:
                    x, y, w, h = map(float, parts[:4])
                    if w > 0 and h > 0:
                        bboxes.append((x, y, w, h))
                except:
                    pass
            i += 1

        if not os.path.exists(image_path):
            print(f"⚠️ Missing image: {image_rel_path}")
        elif not bboxes:
            print(f"⚠️ No valid annotations for: {image_rel_path}")
        else:
            create_xml(image_path, image_rel_path, bboxes)

parse_annotations()