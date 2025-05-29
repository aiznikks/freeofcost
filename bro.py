import os
import glob
import pandas as pd
import tensorflow as tf
import xml.etree.ElementTree as ET
from collections import namedtuple
from object_detection.utils import dataset_util

# Set paths
XML_DIR = "annotations_xml"
IMAGE_DIR = "WIDER_train/images"
TFRECORD_OUTPUT_PATH = "train.record"
LABEL_MAP = {"face": 1}

def xml_to_csv(xml_dir):
    xml_list = []
    for xml_file in glob.glob(os.path.join(xml_dir, "*.xml")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename = root.find('filename').text
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)

            for member in root.findall('object'):
                class_name = member.find('name').text
                if class_name not in LABEL_MAP:
                    continue
                bndbox = member.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                xml_list.append((filename, width, height, class_name, xmin, ymin, xmax, ymax))
        except Exception as e:
            print(f"⚠️ Skipping malformed XML: {xml_file} | Error: {e}")
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    return pd.DataFrame(xml_list, columns=column_name)

def class_text_to_int(row_label):
    return LABEL_MAP.get(row_label, None)

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_tf_example(group, path):
    image_path = os.path.join(path, group.filename)
    if not os.path.exists(image_path):
        print(f"⚠️ Missing image: {image_path}")
        return None

    try:
        with tf.io.gfile.GFile(image_path, 'rb') as fid:
            encoded_jpg = fid.read()
    except:
        print(f"⚠️ Failed to read image: {group.filename}")
        return None

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    width = int(group.width.iloc[0])
    height = int(group.height.iloc[0])

    xmins, xmaxs, ymins, ymaxs, classes_text, classes = [], [], [], [], [], []

    for index, row in group.object.iterrows():
        if None in [row.xmin, row.ymin, row.xmax, row.ymax]:
            continue
        xmins.append(row.xmin / width)
        xmaxs.append(row.xmax / width)
        ymins.append(row.ymin / height)
        ymaxs.append(row.ymax / height)
        classes_text.append(row['class'].encode('utf8'))
        class_id = class_text_to_int(row['class'])
        if class_id is None:
            continue
        classes.append(class_id)

    if not classes:
        print(f"⚠️ No valid annotations for {group.filename}")
        return None

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def main():
    writer = tf.io.TFRecordWriter(TFRECORD_OUTPUT_PATH)
    examples = xml_to_csv(XML_DIR)
    grouped = split(examples, 'filename')
    print(f"📦 Found {len(grouped)} image groups.")

    count = 0
    for group in grouped:
        tf_example = create_tf_example(group, IMAGE_DIR)
        if tf_example:
            writer.write(tf_example.SerializeToString())
            count += 1

    writer.close()
    print(f"TFRecord created: {TFRECORD_OUTPUT_PATH} with {count} valid records.")

if __name__ == '__main__':
    main()