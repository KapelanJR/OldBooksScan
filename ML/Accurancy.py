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
    test_dir,target_size=(20,32),batch_size=71,class_mode='categorical'
)

model = models.load_model("./test_new.h5")
pred = model.predict_generator(test_generator,steps=test_generator.n//test_generator.batch_size)

#tablica z przewiywanymi wartosciami
li = []

model = models.load_model("./test.h5")
#scores = model.evaluate_generator(test_generator,10000)
pred = model.predict_generator(test_generator,steps=2)


#tablica z wartosciami jakie maja byc
vi = []
for x in test_generator.classes:
    vi.append(fi[x])
        
print(classification_report(vi, li))
