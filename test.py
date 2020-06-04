from keras import layers
from keras import models
from keras.preprocessing import image
import os,shutil
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras import optimizers
from keras import regularizers
from sklearn.metrics import classification_report
from keras.models import load_model

#Klasa posiadająca dane o danym znaku
class charData:
    def __init__(self, char, unicode):
        self.char = char
        self.unicode = unicode
        self.count = 0


def MakeSets(train_dir,test_dir,validation_dir,base_dir):
    #Lista znaków
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

    #Spacja
    charData(' ', "0020"),

    ]

    for char in charList:
        fnames = ['{}_{}.jpg'.format(char.unicode,i) for i in range(1,3001)]
        for fname in fnames:
            dst = os.path.join(base_dir,fname)
            if(os.path.exists(dst)):
                char.count +=1
            else:
                break


    #Kopiowoanie danej liczby zdjęć do poszczególnych folderów
    for char in charList:
        fnames = ['{}_{}.jpg'.format(char.unicode,i) for i in range(1,int(0.75*char.count)) ]
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(train_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                break

    for char in charList:
        fnames = ['{}_{}.jpg'.format(char.unicode,i) for i in range(int(0.75*char.count),int(0.95*char.count)) ]
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(validation_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                break

    for char in charList:
        fnames = ['{}_{}.jpg'.format(char.unicode,i) for i in range(int(0.95*char.count),int(char.count)) ]
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(test_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                break

        


def main():
    #Ścieżki do folderów używanych przy trenowaniu, walidacji i testowaniu
    base_dir = 'C:\\Users\\Marcin\\Desktop\\Studia\\Projekt_PW\\Kod\\TFS\\datasetsGenerator\\datasets\\polish_1'

    train_dir = os.path.join(base_dir,'train')
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)

    validation_dir = os.path.join(base_dir,'validation')
    if not os.path.exists(validation_dir):
        os.mkdir(validation_dir)

    test_dir = os.path.join(base_dir,'test')
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)


    #MakeSets(train_dir,test_dir,validation_dir,base_dir)


    #Generatory zwracające wszystkie pliki z danego foldera i jego podfolderów
    #Podfolder jest traktowany jako odzielna etykeita
    #Przeskalowane z 3 wymiarów (RGB) do 1 wymiaru 
    train_datagen = ImageDataGenerator(
        rescale=1./290
    )
    test_datagen = ImageDataGenerator(rescale=1./290)

    train_generator = train_datagen.flow_from_directory(
        train_dir,target_size=(50,64),batch_size=420,class_mode='categorical'
    )

    validation_generator = test_datagen.flow_from_directory(
        validation_dir,target_size=(50,64),batch_size=420,class_mode='categorical'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,target_size=(50,64),batch_size=420,class_mode='categorical'
    )


    

    #Architektura sieci
    model = models.Sequential()
    model.add(layers.Conv2D(128,(3,3),activation='relu',input_shape=(50,64,3)))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Conv2D(128,(3,3),activation='relu'))
    model.add(layers.MaxPool2D((2,2)))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(512,activation='relu', kernel_regularizer=regularizers.l2(0.001)))
    model.add(layers.Dense(90,activation='softmax'))

    model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])


    history = model.fit_generator(
        train_generator,
        steps_per_epoch=428,
        epochs=30,
        validation_data=validation_generator,
        validation_steps=116
    )


    #Wykresiki
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epchos = range(len(acc))

    model.save('c295.h5')

    plt.plot(epchos,acc,'bo',label="Dokładność trenowania")
    plt.plot(epchos, val_acc,'b',label="Dokładność walidacji")
    plt.title('Dokładnośc trenownia i walidacji')
    plt.legend()

    plt.figure()

    plt.plot(epchos,loss,'bo',label="Strata trenowania")
    plt.plot(epchos, val_loss,'b',label="Strata walidacji")
    plt.title('Strata trenowania i walidacji')
    plt.legend()

    plt.show()



if __name__ == "__main__":
    main()