import os
import cv2
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

ANNOTATION_FILE = "wider_face_split/wider_face_train_bbx_gt.txt"
IMAGE_DIR = "WIDER_train/images"
OUTPUT_DIR = "annotations_xml"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_xml(image_path, image_name, bboxes):
    img = cv2.imread(image_path)
    height, width, depth = img.shape

    annotation = Element('annotation')
    SubElement(annotation, 'folder').text = 'WIDER_train'
    SubElement(annotation, 'filename').text = image_name
    SubElement(annotation, 'path').text = image_path

    size = SubElement(annotation, 'size')
    SubElement(size, 'width').text = str(width)
    SubElement(size, 'height').text = str(height)
    SubElement(size, 'depth').text = str(depth)

    for bbox in bboxes:
        obj = SubElement(annotation, 'object')
        SubElement(obj, 'name').text = 'face'
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'

        bndbox = SubElement(obj, 'bndbox')
        SubElement(bndbox, 'xmin').text = str(int(bbox[0]))
        SubElement(bndbox, 'ymin').text = str(int(bbox[1]))
        SubElement(bndbox, 'xmax').text = str(int(bbox[0] + bbox[2]))
        SubElement(bndbox, 'ymax').text = str(int(bbox[1] + bbox[3]))

    rough_string = tostring(annotation, 'utf-8')
    reparsed = parseString(rough_string)
    with open(os.path.join(OUTPUT_DIR, image_name.replace('.jpg', '.xml')), 'w') as f:
        f.write(reparsed.toprettyxml(indent="  "))

def parse_annotations():
    with open(ANNOTATION_FILE, 'r') as f:
        lines = f.readlines()

    i = 0
    total = len(lines)
    while i < total:
        image_rel_path = lines[i].strip()
        image_path = os.path.join(IMAGE_DIR, image_rel_path)
        image_name = os.path.basename(image_path)
        i += 1

        face_count = int(lines[i].strip())
        i += 1

        bboxes = []
        for _ in range(face_count):
            parts = lines[i].strip().split()
            if len(parts) >= 4:
                x, y, w, h = map(float, parts[:4])
                if w > 0 and h > 0:
                    bboxes.append((x, y, w, h))
            i += 1

        if os.path.exists(image_path) and bboxes:
            try:
                create_xml(image_path, image_name, bboxes)
            except:
                print(f"❌ Error processing: {image_path}")

parse_annotations()