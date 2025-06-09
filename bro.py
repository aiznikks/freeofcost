import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

loaded = tf.saved_model.load("your_saved_model_dir")
concrete_func = loaded.signatures['serving_default']

frozen_func = convert_variables_to_constants_v2(concrete_func)
graph_def = frozen_func.graph.as_graph_def()

# Save frozen graph
with tf.io.gfile.GFile("frozen_model.pb", "wb") as f:
    f.write(graph_def.SerializeToString())