import tensorflow as tf

# Load original .pb
with tf.io.gfile.GFile("resnetv1_50.pb", "rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Rewrite graph with static input shape
with tf.Graph().as_default() as graph:
    # Replace 'InputImage' with your actual input node name
    input_tensor = tf.compat.v1.placeholder(dtype=tf.float32, shape=[1, 224, 224, 3], name="InputImage")
    tf.compat.v1.import_graph_def(graph_def, input_map={"InputImage": input_tensor}, name="")

    # Save the new static model as frozen .pb
    with tf.compat.v1.Session(graph=graph) as sess:
        output_graph_def = tf.compat.v1.graph_util.convert_variables_to_constants(
            sess,
            sess.graph_def,
            output_node_names=["final_output_node_name"]  # Replace with actual output node name
        )

        with tf.io.gfile.GFile("resnetv1_50_static.pb", "wb") as f:
            f.write(output_graph_def.SerializeToString())