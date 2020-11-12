import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    from keras.models import load_model
    from keras import models
    import numpy as np
    from keras.preprocessing.image import load_img,img_to_array
import os,shutil
import unicodedata
import mysql.connector
from SingleUseFunctions import charData,charList,database_connection
import pandas as pd
import json

def pred_img(model,path,labels):
    img = load_img(path=path,target_size=(20,32))
    input_arr = img_to_array(img)
    input_arr = np.array([input_arr])
    pred = model.predict(input_arr)
    #Pobranie litery z najwiekszym prawdopodobienstwem
    for i in pred:
        return labels[str(np.argmax(i))]



def main():
    #mycursor = database_connection("10.8.0.1","kacper","5fUwXohpL6rh5xvK","baza_wynikowa")
    #mycursor.execute('SELECT sciezka,litera_id FROM litery')
    #letters = mycursor.fetchall()

    model = models.load_model("./test.h5")

    #Pobranie etykiet z pliku
    labels = {}
    with open('./labels.txt', 'r') as file:
        labels = json.load(file)
    path = "./polish_1_hd/test/00d3/00d3_1083.jpg"
    print(pred_img(model,path,labels))
    
    #for letter in letters:
        #letter[1] sciezka letter[0] id
        #wez zdjecie podaj do model.predict() i wynik zapisz w letter[0] w db

    #mycursor.close()


if __name__ == "__main__":
    main()