from keras import layers
from keras import models
from keras.preprocessing import image
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras import regularizers
from sklearn.metrics import classification_report,confusion_matrix
from keras.models import load_model
import pandas as pd

  
train_dir = "readyDatasets/cleaned/polish1/train"
validation_dir = "readyDatasets/cleaned/polish1/validation"
test_dir = "readyDatasets/cleaned/polish1/test"
#Generatory zwracające wszystkie pliki z danego foldera i jego podfolderów
#Podfolder jest traktowany jako odzielna etykeita
#Przeskalowane z 3 wymiarów (RGB) do 1 wymiaru 
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,target_size=(20,32),batch_size=90,class_mode='categorical',shuffle=True
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,target_size=(20,32),batch_size=90,class_mode='categorical',shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,target_size=(20,32),batch_size=10000,class_mode='categorical',shuffle=True)

#Architektura sieci
model = models.Sequential()
model.add(layers.Conv2D(256,(3,3),activation='relu',input_shape=(20,32,3)))
model.add(layers.MaxPool2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(256,activation='relu'))
model.add(layers.Dense(1024,activation='relu'))
model.add(layers.Dense(88,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.n//train_generator.batch_size,
    epochs=7,
    validation_data=validation_generator,
    validation_steps=validation_generator.n//validation_generator.batch_size,
)

# Evaluate trained model


score = model.evaluate_generator(test_generator,10000)

model.save("{}_test1.h5".format(score))

