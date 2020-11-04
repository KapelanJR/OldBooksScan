from sklearn.metrics import classification_report,confusion_matrix
from keras.models import load_model
from keras import models
from keras.preprocessing import image
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import unicodedata
import mysql.connector

def main():
    x = 0
    mydb = mysql.connector.connect(
    host="10.8.0.1",
    user="kacper",
    password="5fUwXohpL6rh5xvK"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)

if __name__ == "__main__":
    main()