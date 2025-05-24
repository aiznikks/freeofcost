from keras_centernet.models.networks.hourglass import HourglassNetwork
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

heads = {
    'hm': 80,
    'reg': 2,
    'wh': 2
}

kwargs = {
    'num_stacks': 2,
    'cnv_dim': 256,
    'weights': 'ctdet_coco_hg.hdf5',  # Make sure this path is correct
    'inres': (512, 512),
}

model = HourglassNetwork(heads=heads, **kwargs)
model.save("centernet_model.h5")
print("✅ Model saved as centernet_model.h5")
