import tensorflow as tf

# Paths
frozen_graph_path = "model.pb"
saved_model_dir = "face_ssd_saved_model"

# Load frozen graph
with tf.io.gfile.GFile(frozen_graph_path, "rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Import graph into default graph
with tf.Graph().as_default() as graph:
    tf.import_graph_def(graph_def, name="")

# Print inputs and outputs to double-check
for op in graph.get_operations():
    print(op.name)

# Now save as SavedModel
with tf.compat.v1.Session(graph=graph) as sess:
    tf.compat.v1.saved_model.simple_save(
        sess,
        saved_model_dir,
        inputs={"image_tensor": graph.get_tensor_by_name("image_tensor:0")},
        outputs={
            "detection_boxes": graph.get_tensor_by_name("detection_boxes:0"),
            "detection_scores": graph.get_tensor_by_name("detection_scores:0"),
            "detection_classes": graph.get_tensor_by_name("detection_classes:0"),
            "num_detections": graph.get_tensor_by_name("num_detections:0"),
        },
    )

print("✅ SavedModel created at:", saved_model_dir)