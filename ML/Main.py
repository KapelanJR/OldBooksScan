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
import json

# model = trained keras model ||  path = path to image || labels = file with all possible labels
def pred_img(model,path,labels):
    img = load_img(path=path,target_size=(20,32))
    input_arr = img_to_array(img)
    input_arr = np.array([input_arr])
    pred = model.predict(input_arr)
    #Pobranie litery z najwiekszym prawdopodobienstwem
    for i in pred:
        return labels[str(np.argmax(i))]

def uni_to_char(unicode):
    for uni in charList:
        if (uni.unicode == unicode):
            return uni.char

def main():
    sql_update = "UPDATE litery SET predykcja = %s WHERE id = %s"
    db = database_connection("10.8.0.1","kacper","5fUwXohpL6rh5xvK","baza_wynikowa")
    mycursor = db.cursor()
    #Getting all letters to predict
    mycursor.execute('SELECT sciezka,litera_id FROM litery WHERE predykcja IS NULL LIMIT 100')
    letters = mycursor.fetchall()

    model = models.load_model("./test_new.h5")

    #Loading labels from file
    labels = {}
    with open('./labels.txt', 'r') as file:
        labels = json.load(file)

    #Predict all images in db
    for letter in letters:
        #letter[0] = path || letter[1] = id
        pred = pred_img(model,letter[0],labels)
        pred = uni_to_char(pred)
        mycursor.execute(sql_update,(pred,letter[1]))

    mycursor.close()


if __name__ == "__main__":
    main()