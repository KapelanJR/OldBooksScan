import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    from keras.models import load_model
    from keras import models
    from keras.preprocessing import image
    import numpy as np
    from keras.preprocessing.image import ImageDataGenerator
    from sklearn.metrics import classification_report,confusion_matrix
import os,shutil
import unicodedata
import mysql.connector
from SingleUseFunctions import charData,charList,database_connection
import pandas as pd
import cv2



def main():
    #mycursor = database_connection("10.8.0.1","kacper","5fUwXohpL6rh5xvK","baza_wynikowa")
    #mycursor.execute('SELECT sciezka,litera_id FROM litery')
    #letters = mycursor.fetchall()

    #Reading labaels
    chars = []
    for char in charList:
        chars.append(char.char)
    chars = sorted(chars)

    model = models.load_model("./ML//test.h5")

    img = cv2.imread('./ML//5.png')
    img = cv2.resize(img,(20,32))
    img = np.reshape(img,[1,20,32,3])
    pred = model.predict_classes(img)


    print(chars[int(pred-1)])
    
    #for letter in letters:
        #letter[1] sciezka letter[0] id
        #wez zdjecie podaj do model.predict() i wynik zapisz w letter[0] w db

    #mycursor.close()


if __name__ == "__main__":
    main()