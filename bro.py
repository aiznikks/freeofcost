import os
import glob
import pandas as pd
import tensorflow as tf
import xml.etree.ElementTree as ET
from object_detection.utils import dataset_util

flags = tf.compat.v1.app.flags
flags.DEFINE_string('xml_dir', 'annotations_xml', 'Path to the XML annotations')
flags.DEFINE_string('image_dir', 'WIDER_train/images', 'Path to images')
flags.DEFINE_string('output_path', 'train.record', 'Path to output TFRecord')
flags.DEFINE_string('label_map_path', 'label_map.pbtxt', 'Path to label map')
FLAGS = flags.FLAGS

def xml_to_csv(xml_dir):
    xml_list = []
    for xml_file in glob.glob(xml_dir + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (
                root.find('filename').text,
                int(root.find('size')[0].text),
                int(root.find('size')[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text)
            )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    return pd.DataFrame(xml_list, columns=column_name)

def class_text_to_int(row_label):
    if row_label == 'face':
        return 1
    else:
        return None

def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    width = int(group.width.iloc[0])
    height = int(group.height.iloc[0])

    xmins, xmaxs, ymins, ymaxs, classes_text, classes = [], [], [], [], [], []

    for index, row in group.object.iterrows():
        xmins.append(row.xmin / width)
        xmaxs.append(row.xmax / width)
        ymins.append(row.ymin / height)
        ymaxs.append(row.ymax / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

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

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

from collections import namedtuple

def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.output_path)
    path = FLAGS.image_dir
    examples = xml_to_csv(FLAGS.xml_dir)
    grouped = split(examples, 'filename')

    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    print(f"✅ Successfully created TFRecord at: {FLAGS.output_path}")

if __name__ == '__main__':
    tf.compat.v1.app.run()