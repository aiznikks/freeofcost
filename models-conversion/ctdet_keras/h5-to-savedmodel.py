from tensorflow.keras.models import load_model

model = load_model("centernet_model.h5", compile=False)
model.save("centernet_saved_model")
print("✅ SavedModel exported")
