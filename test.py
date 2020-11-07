from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers, optimizers
import os,shutil
import numpy as np
import mysql.connector
from keras_preprocessing.image import ImageDataGenerator
import pandas as pd
from keras.models import Sequential
from keras import models
from keras import layers
from keras.models import load_model

def append_ext(fn):
    return fn+".jpg"

def main():
    '''
    mydb = mysql.connector.connect(
    host="192.168.1.250",
    user="kacper",
    password="5fUwXohpL6rh5xvK",
    database="baza_do_nauki"
    )


    mycursor = mydb.cursor()
    mycursor.execute("SELECT sciezka FROM znaki")
    images = mycursor.fetchall()
    '''


    traindf = pd.read_csv("./TrainLabels.csv",dtype=str)

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

    #Architektura sieci
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
    """
    for i,image in enumerate(images):
        with sftp.open(image[0]) as f:
            file = f.read()




    with sftp.open("/var/lib/tfs/training/datasets/polish_1_hd/0075_351.jpg") as f:
        img = cv2.imdecode(np.fromstring(f.read(), np.uint8), 1)

    cv2.imshow("image", img)
    cv2.waitKey(0)
    """


if __name__ == "__main__":
    main()
