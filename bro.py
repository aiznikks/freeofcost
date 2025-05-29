def create_tf_example(group, path):
    image_path = os.path.join(path, group.filename)

    # ✅ Try/Except block to skip missing images
    try:
        with tf.io.gfile.GFile(image_path, 'rb') as fid:
            encoded_jpg = fid.read()
    except:
        print(f"⚠️ Skipping missing file: {group.filename}")
        return None

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
        classes.append(1)  # Only one class: face

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