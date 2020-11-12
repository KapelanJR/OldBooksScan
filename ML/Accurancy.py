from sklearn.metrics import classification_report,confusion_matrix
from keras.models import load_model
from keras import models
from keras.preprocessing import image
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

for a, i in enumerate(pred):
    for x,y in test_generator.class_indices.items():
        if(y == np.argmax(i)): 
            li.append(x)
            break

#tablica z odwzorowaniem zakodowanych id na nasze unicody
fi = []
for x,y in test_generator.class_indices.items():
    fi.append(x)

#tablica z wartosciami jakie maja byc
vi = []
for x in test_generator.classes:
    vi.append(fi[x])
        
print(classification_report(vi, li))