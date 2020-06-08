from sklearn.metrics import classification_report,confusion_matrix
from keras.models import load_model
from keras import models
from keras.preprocessing import image
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import unicodedata



#Klasa posiadająca dane o danym znaku
class charData:
    def __init__(self, char, unicode):
        self.char = char
        self.unicode = unicode
        self.count = 0

charList = [

    #Małe lietry
    charData('a', "0061"), charData('b', "0062"), charData('c', "0063"), charData('d', "0064"), charData('e', "0065"), charData('f', "0066"), charData('g', "0067"), charData('h', "0068"), charData('i', "0069"), charData('j', "006a"), charData('k', "006b"), charData('l', "006c"), charData('m', "006d"), charData('n', "006e"), charData('o', "006f"), charData('p', "0070"), charData('r', "0072"), charData('s', "0073"), charData('t', "0074"), charData('u', "0075"), charData('w', "0077"), charData('y', "0079"), charData('z', "007a"), 

    #Małe lietry polskie
    charData('ą', "0105"), charData('ć', "0107"), charData('ę', "0119"), charData('ł', "0142"), charData('ń', "0144"), charData('ó', "00f3"), charData('ś', "015b"), charData('ź', "017a"), charData('ż', "017c"), 

    #Małe litery angielskie 
    #charData('q', "0071"), charData('v', "0076"), charData('x', "0078"),

    #Duże litery
    charData('A', "0041"), charData('B', "0042"), charData('C', "0043"), charData('D', "0044"), charData('E', "0045"), charData('F', "0046"), charData('G', "0047"), charData('H', "0048"), charData('I', "0049"), charData('J', "004a"), charData('K', "004b"), charData('L', "004c"), charData('M', "004d"), charData('N', "004e"), charData('O', "004f"), charData('P', "0050"), charData('R', "0052"), charData('S', "0053"), charData('T', "0054"), charData('U', "0055"), charData('W', "0057"), charData('Y', "0059"), charData('Z', "005a"), 

    #Duże lietry polskie
    charData('Ą', "0104"), charData('Ć', "0106"), charData('Ę', "0118"), charData('Ł', "0141"), charData('Ń', "0143"), charData('Ó', "00d3"), charData('Ś', "015a"), charData('Ź', "0179"), charData('Ż', "017b"), 

    #Duże litery angielskie 
    #charData('Q', "0051"), charData('V', "0056"), charData('X', "0058"),

    #Liczby
    charData('0', "0030"), charData('1', "0031"), charData('2', "0032"), charData('3', "0033"), charData('4', "0034"), charData('5', "0035"), charData('6', "0036"), charData('7', "0037"), charData('8', "0038"), charData('9', "0039"),

    #Inne znaki 
    charData('!', "0021"), charData('?', "003f"), charData(',', "002c"), charData('.', "002e"), charData('(', "0028"), charData(')', "0029"), charData(':', "003a"), charData('-', "002d"), 
    
    #Inne znaki rzadkie
    charData('+', "002b"), charData('=', "003d"), charData('*', "002a"), charData('/', "002f"), charData(';', "003b"),

    #Inne znaki bardzo rzadkie
    #charData('%', "0025"), charData('^', "005e"), charData('$', "0024"), charData('&', "0026"), charData('#', "0023"), charData('<', "003c"), charData('>', "003e"), charData('\\', "003e"), 

    #Inne znaki polskie
    charData('”', "201d"), charData('„', "201e"), 

    #Inne znaki angielskie
    #charData('"', "0022"), charData('\'', "0027")


    ]



def Encode(data):
    for char in charList:
        if(char.unicode == data):
            return char.char

def getClasses():
    test_dir = 'D:\\Progamowanie Python\\Uczenie Maszynowe\\datasetsGenerator\\datasets\\Etykiety'

    #Wczytanie etykiet klas
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_directory(
        test_dir,target_size=(20,32),batch_size=1,class_mode='categorical'
        )

    return test_generator.class_indices.items()


def getNumOfFolders(path,f):
    num = 0
    for root,dirs,files in os.walk(path):
        if (root[len(path):].count(os.sep) < 1 and f!=1):
            num = len(dirs)
        elif(root[len(path):].count(os.sep) < 1):
            num = len(files)
    return num


def toNormal(pred,classes):
    #Zamiana przewidywań na unicody
    result = []
    for a, i in enumerate(pred):
        for x,y in classes:
            if((y-1) == np.argmax(i)): 
                result.append(Encode(x))
                break
    return result

def getUnicode(pred,classes):
    #Zamiana id na unicody
    result = []
    for a, i in enumerate(pred):
        for x,y in classes:
            if((y-1) == np.argmax(i)): 
                result.append(x)
                break
    return result

def main():

    base_dir = 'D:\\Progamowanie Python\\Uczenie Maszynowe\\datasetsGenerator\\datasets\\gen'

    result_dir = 'D:\\Progamowanie Python\\Uczenie Maszynowe\\Results'

    classes = getClasses()

    #Generowanie kolejno zdjec liter z folderu
    gen = ImageDataGenerator(rescale=1./255)

    #Wczytanie modeku
    model = models.load_model("(BEST)256__256_1024_6.h5")

    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(base_dir)))

    num_of_books = getNumOfFolders(base_dir,0)

    #iteracja po folderach ksiazek
    for book in range(1,(num_of_books+1)):
        book_path = os.path.join(base_dir,str(book))
        result_path = os.path.join(result_dir,str(book))
        if not os.path.exists(result_path):
            os.mkdir(result_path)
        num_of_pages = getNumOfFolders(book_path,0)
        #iteracja po folderach stron
        for page in range(1,(num_of_pages+1)):
            page_path = os.path.join(book_path,str(page))
            filename = os.path.join(result_path,str(page)+'.txt')
            if os.path.exists(filename):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not
            res = open(filename,append_write)
            num_of_lines = getNumOfFolders(page_path,0)
            #iteracja po folderach linii
            for line in range(1,(num_of_lines+1)):
                line_path = os.path.join(page_path,str(line))
                num_of_words = getNumOfFolders(line_path,0)
                #iteracja po folderach słów
                for word in range(1,(num_of_words+1)):
                    word_path = os.path.join(line_path,str(word))
                    word_path_1 = os.path.join(word_path,'Nowy folder')
                    num_of_letters = getNumOfFolders(word_path_1,1)

                    generator = gen.flow_from_directory(
                    word_path,target_size=(20,32),batch_size=1,class_mode='categorical',shuffle=False
                    )

                    pred = model.predict_generator(generator,steps=num_of_letters)
                    if(getUnicode(pred,classes)!= None):
                        files = toNormal(pred,classes)
                        for i in files:
                            res.write(i)
                    res.write(' ')
                res.write('\n')
        



if __name__ == "__main__":
    main()