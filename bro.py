#to freeze model
import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

loaded = tf.saved_model.load("your_saved_model_dir")
concrete_func = loaded.signatures['serving_default']

frozen_func = convert_variables_to_constants_v2(concrete_func)
graph_def = frozen_func.graph.as_graph_def()

# Save frozen graph
with tf.io.gfile.GFile("frozen_model.pb", "wb") as f:
    f.write(graph_def.SerializeToString())
    
    
    
#to check input output or saved model
saved_model_cli show --dir /path/to/saved_model_folder --all



#
[one-import-tf]
input_path=/path/to/saved_model_folder
output_path=resnet_v2_50.circle
input_arrays=serving_default_inputs
output_arrays=StatefulPartitionedCall
input_shapes=serving_default_inputs[1,224,224,3]

[one-optimize]
input_path=resnet_v2_50.circle
output_path=resnet_v2_50_optimized.circle

[one-codegen]
input_path=resnet_v2_50_optimized.circle
output_path=resnet_v2_50.tvn