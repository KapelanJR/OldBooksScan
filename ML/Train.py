import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    from keras_preprocessing.image import ImageDataGenerator
    from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
    from keras.layers import Conv2D, MaxPooling2D
    from keras import regularizers, optimizers
    import numpy as np
    from keras.models import Sequential
    from keras import models
    from keras import layers
import os,shutil
import mysql.connector
import pandas as pd
from SingleUseFunctions import create_CSV,database_connection


def append_ext(fn):
    return fn+".jpg"

def main():
    '''
    mycursor = database_connection("192.168.1.250","kacper","5fUwXohpL6rh5xvK","baza_do_nauki")
    mycursor.execute("SELECT sciezka FROM znaki")
    images = mycursor.fetchall()
    '''

    #If u dont have CSV file with labales use create_CSV function
    #and pass tupple of absolute paths to files
    traindf = pd.read_csv("./ML//TrainLabels.csv",dtype=str)

    traindf["id"]=traindf["id"].apply(append_ext)
    datagen=ImageDataGenerator(rescale=1./255,validation_split=0.25)


    train_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory= "./datasetsGenerator/datasets/polish_1_hd",
        x_col="id",
        y_col="label",
        subset="training",
        batch_size=90,
        shuffle=False,
        class_mode="categorical",
        target_size=(20,32)
    )

    valid_generator=datagen.flow_from_dataframe(
        dataframe=traindf,
        directory= "./datasetsGenerator/datasets/polish_1_hd",
        x_col="id",
        y_col="label",
        subset="validation",
        batch_size=90,
        shuffle=False,
        class_mode="categorical",
        target_size=(20,32)
    )
    print(len(train_generator.class_indices.items()))
    return
    #Network architecture
    model = models.Sequential()
    model.add(layers.Conv2D(256,(3,3),activation='relu',input_shape=(20,32,3)))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(256,activation='relu'))
    model.add(layers.Dense(1024,activation='relu'))
    model.add(layers.Dense(88,activation='softmax'))

    model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])


    STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
    STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size

    history = model.fit_generator(
        generator=train_generator,
        steps_per_epoch=STEP_SIZE_TRAIN,
        validation_data=valid_generator,
        validation_steps=STEP_SIZE_VALID,
        epochs=6
    )

    model.save("test.h5")


if __name__ == "__main__":
    main()