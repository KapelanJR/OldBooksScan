from sklearn.metrics import classification_report,confusion_matrix
from keras.models import load_model
from keras import models
from keras.preprocessing import image
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from SingleUseFunctions import *
from os import listdir
from os.path import isfile, join

#Directory with stored files
dir = "./"

files = [f for f in listdir(dir) if isfile(join(dir, f))]

create_CSV(files,"")

traindf = pd.read_csv("./TrainLabels.csv",dtype=str)
traindf["id"]=traindf["id"].apply(append_ext)
datagen=ImageDataGenerator(rescale=1./255)

model = models.load_model("./test.h5")

test_generator=datagen.flow_from_dataframe(
    dataframe=traindf,
    directory= "./datasetsGenerator/datasets/test",
    x_col="id",
    y_col="label",
    batch_size=90,
    shuffle=False,
    class_mode="categorical",
    target_size=(20,32)
)

pred = model.predict_generator(test_generator, steps=test_generator.n//test_generator.batch_size)


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