import warnings  
with warnings.catch_warnings():  
    from sklearn.metrics import classification_report,confusion_matrix
    from keras.models import load_model
    from keras import models
    from keras.preprocessing import image
    from keras.preprocessing.image import ImageDataGenerator
    import numpy as np
import os,shutil
import json


test_dir = './polish_1_hd/test'


test_datagen = ImageDataGenerator(
    rescale=1./255
)

test_generator = test_datagen.flow_from_directory(
    test_dir,target_size=(20,32),batch_size=2,class_mode='categorical',shuffle=False)

model = models.load_model("./test.h5")
#scores = model.evaluate_generator(test_generator,10000)
pred = model.predict_generator(test_generator,steps=2)


# Zamiana kluczy z wartościani wynik {indeks:unicode litery}
inv_map = {v: k for k, v in test_generator.class_indices.items()}
with open('./labels.txt', 'w') as file:
    json.dump(inv_map, file)

for i in pred:
    print(inv_map[np.argmax(i)])
