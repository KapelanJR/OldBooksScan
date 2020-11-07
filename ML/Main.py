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



def main():
    #mycursor = database_connection("192.168.1.250","kacper","5fUwXohpL6rh5xvK","baza_do_nauki")

    #Reading all labels from CSV file
    labels = pd.read_csv("./ML//TrainLabels.csv",dtype=str)
    labels = labels['label'].unique()
    print(labels)
    #model = models.load_model("(BEST)256__256_1024_6.h5")


if __name__ == "__main__":
    main()