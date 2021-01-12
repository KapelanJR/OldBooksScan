import warnings

from keras.layers.merge import Average  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    from keras.models import load_model
    from keras import models
    import numpy as np
    from keras.preprocessing.image import load_img,img_to_array
import os,shutil
import unicodedata
import mysql.connector
from SingleUseFunctions import charData, charList, database_connection,check_word
from ORM.OrmModels import *
import json
import functools
import time
import threading

# model = trained keras model ||  path = path to image || labels = file with all possible labels
def PredImg(model,path,labels):
    img = load_img(path=path,target_size=(20,32))
    input_arr = img_to_array(img)
    input_arr = np.array([input_arr])
    pred = model.predict(input_arr)
    #Pobranie litery z najwiekszym prawdopodobienstwem
    for i in pred:
        return labels[str(np.argmax(i))]

def UniToChar(unicode):
    for uni in charList:
        if (uni.unicode == unicode):
            return uni.char


def Dictionary(book,cursor):
    cursor.execute('SELECT l.predykcja,l.litera_id,w.wyraz_id FROM litery l JOIN wyrazy w on w.wyraz_id = l.wyraz_id JOIN linie li ON li.linia_id = w.wyraz_id JOIN strony s on s.strona_id = li.strona_id JOIN ksiazki k on k.ksiazka_id = s.ksiazka_id WHERE k.nazwa = "{}" ORDER BY w.wyraz_id'.format(book))
    letters = cursor.fetchall()
    updateList = []
    #[0] predyction [1] liId [2] wordId
    word = letters[0][0]
    ids = [letters[0][1]]
    prevId = letters[0][2]
    for n in range(1,len(letters)):
        if(letters[n][2] != prevId):
            word = check_word(word)
            
            for k in range(len(word)):
                updateList.append((word[k], ids[k]))
                #cursor.execute('UPDATE litery SET predykcja_slownik = "{}" WHERE litera_id = {} AND predykcja_slownik IS NULL'.format(word[k], ids[k]))
            word = letters[n][0]
            ids = [letters[n][1]]
            prevId = letters[n][2]
        else:
            word += letters[n][0]
            ids.append(letters[n][1])
            prevId = letters[n][2]
    cursor.executemany(
        "UPDATE litery SET predykcja_slownik = %s WHERE litera_id = %s AND predykcja_slownik IS NULL",updateList)


def WordOnPages(book, cursor, chartSqlString,bookId,n):
    chartData = WordsOnPages(book)
    #Add chart to db
    cursor.execute(chartSqlString.format(bookId, n))
    #Get added chart id
    cursor.execute(
      'SELECT w.wykres_id FROM wykresy w WHERE w.ksiazka_id = {}'.format(bookId))
    chartId = cursor.fetchall()[n-1]

    for i in range(len(chartData)):
        chartData[i] = chartId + chartData[i]
    cursor.executemany(
        "INSERT INTO wartosci(wykres_id,x,y) VALUES(%s,%s,%s)", chartData)


def LettersPerPage(book, cursor, chartSqlString, bookId,n):
    chartData = LettersOnPages(book)
    #Add chart to db
    cursor.execute(chartSqlString.format(bookId, n))
    #Get added chart id
    cursor.execute(
        'SELECT w.wykres_id FROM wykresy w WHERE w.ksiazka_id = {}'.format(bookId))
    chartId = cursor.fetchall()[n-1]

    for i in range(len(chartData)):
        chartData[i] = chartId + chartData[i]
    cursor.executemany(
        "INSERT INTO wartosci(wykres_id,x,y) VALUES(%s,%s,%s)", chartData)


def LettersInBooks(book, cursor, chartSqlString, bookId, n):
    chartData = LettersInBook(book)
    #Add chart to db
    cursor.execute(chartSqlString.format(bookId, n))
    #Get added chart id
    cursor.execute(
        'SELECT w.wykres_id FROM wykresy w WHERE w.ksiazka_id = {}'.format(bookId))
    chartId = cursor.fetchall()[n-1]

    for i in range(len(chartData)):
        chartData[i] = chartId + chartData[i]
    cursor.executemany(
        "INSERT INTO wartosci(wykres_id,x,y) VALUES(%s,%s,%s)", chartData)


def AverageWordLen(book, cursor, chartSqlString, bookId, n):
    chartData = LenOfWords(book)
    res = []
    #Add chart to db
    cursor.execute(chartSqlString.format(bookId, n))
    #Get added chart id
    cursor.execute(
        'SELECT w.wykres_id FROM wykresy w WHERE w.ksiazka_id = {}'.format(bookId))
    chartId = cursor.fetchall()[n-1]

    prevPage = chartData[0][0]
    counter = 0.0
    sumLen = 0.0
    for n in range(1,len(chartData)):
        #End of page
        if(prevPage != chartData[n][0]):
            res.append((prevPage,sumLen/counter,))
            counter = 0.0
            sumLen = 0.0
        counter += 1
        sumLen += chartData[n][1]
        prevPage = chartData[n][0]

    for i in range(len(res)):
        res[i] = chartId + res[i]
    cursor.executemany(
        "INSERT INTO wartosci(wykres_id,x,y) VALUES(%s,%s,%s)", res)

def MakeCharts(book,cursor):
    chartSqlString = 'INSERT INTO wykresy(ksiazka_id,typ_id) VALUES({},{})'
    #Get bookId
    cursor.execute(
        'SELECT k.ksiazka_id FROM ksiazki k WHERE k.nazwa= "{}"'.format(book))
    bookId = cursor.fetchall()[0][0]

    WordOnPages(book,cursor,chartSqlString,bookId,1)
    LettersInBooks(book, cursor, chartSqlString, bookId,2)
    LettersPerPage(book, cursor, chartSqlString, bookId,3)
    AverageWordLen(book, cursor, chartSqlString, bookId, 4)

def Main(book):
    sql_update_pred = "UPDATE litery SET predykcja = %s WHERE litera_id = %s"
    db = database_connection("localhost","tfs","3sHUCwk3)%$%?Q5U","baza_wynikowa")
    mycursor = db.cursor()

    #Getting all letters to predict
    mycursor.execute('SELECT l.sciezka,l.litera_id FROM litery l JOIN wyrazy w ON w.wyraz_id = l.wyraz_id JOIN linie li ON li.linia_id = w.wyraz_id JOIN strony s on s.strona_id = li.strona_id JOIN ksiazki k on k.ksiazka_id = s.ksiazka_id WHERE predykcja IS NULL AND k.nazwa= "{}"'.format(book))
    letters = mycursor.fetchall()

    model = models.load_model("./model.h5")
    
    #Loading labels from file
    labels = {}
    with open('./labels.txt', 'r') as file:
        labels = json.load(file)

    #Predict all images in db
    for letter in letters:
        #letter[0] = path || letter[1] = id
        pred = PredImg(model,letter[0],labels)
        pred = UniToChar(pred)
        mycursor.execute(sql_update_pred,(pred,letter[1]))
    db.commit()

    Dictionary(book, mycursor)
    db.commit()
    MakeCharts(book, mycursor)
    db.commit()
    mycursor.close()
    db.close()

