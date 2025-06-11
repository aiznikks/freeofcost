import tensorflow as tf
from tensorflow.python.platform import gfile

# Load the graph
with tf.compat.v1.Session() as sess:
    with gfile.FastGFile("resnetv1_50.pb", "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name="")

    # Print all operation names
    for op in tf.compat.v1.get_default_graph().get_operations():
        print(op.name)