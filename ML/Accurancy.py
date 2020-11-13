import warnings  
with warnings.catch_warnings():  
    from sklearn.metrics import classification_report,confusion_matrix
    from keras.models import load_model
    from keras import models
    from keras.preprocessing import image
    from keras.preprocessing.image import ImageDataGenerator
    import numpy as np
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from SingleUseFunctions import *

test_dir = "./readyDatasets/polish_1_hd/test"

test_datagen = ImageDataGenerator(
    rescale=1./255
)

test_generator = test_datagen.flow_from_directory(
    test_dir,target_size=(20,32),batch_size=10000,class_mode='categorical',shuffle=True)

model = models.load_model("./test.h5")
scores = model.evaluate_generator(test_generator,10000)
pred = model.predict_generator(test_generator,steps=2)


#tablica z wartosciami jakie maja byc
vi = []
for x in test_generator.classes:
    vi.append(fi[x])
        
print(classification_report(vi, li))
