import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from keras_centernet.models.networks.hourglass import HourglassNetwork

heads = {
    'hm': 80,
    'reg': 2,
    'wh': 2
}

kwargs = {
    'num_stacks': 2,
    'cnv_dim': 256,
    'weights': 'ctdet_coco',
    'inres': (512, 512),
}

model = HourglassNetwork(heads=heads, **kwargs)
model.save("centernet_saved_model")
print(" Keras model exported as 'centernet_saved_model'")
