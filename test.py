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


#Lista znaków

charList = [

    #Małe lietry
    charData('a', "0061"), charData('b', "0062"), charData('c', "0063"), charData('d', "0064"), charData('e', "0065"), charData('f', "0066"),
    charData('g', "0067"), charData('h', "0068"), charData('i', "0069"), charData('j', "006a"), charData('k', "006b"), charData('l', "006c"),
    charData('m', "006d"), charData('n', "006e"), charData('o', "006f"), charData('p', "0070"), charData('r', "0072"), charData('s', "0073"),
    charData('t', "0074"), charData('u', "0075"), charData('w', "0077"), charData('y', "0079"), charData('z', "007a"), 

    #Małe lietry polskie
    charData('ą', "0105"), charData('ć', "0107"), charData('ę', "0119"), charData('ł', "0142"), charData('ń', "0144"), charData('ó', "00f3"),
    charData('ś', "015b"), charData('ź', "017a"), charData('ż', "017c"), 

    #Małe litery angielskie 
    #charData('q', "0071"), charData('v', "0076"), charData('x', "0078"),

    #Duże litery
    charData('A', "0041"), charData('B', "0042"), charData('C', "0043"), charData('D', "0044"), charData('E', "0045"), charData('F', "0046"),
    charData('G', "0047"), charData('H', "0048"), charData('I', "0049"), charData('J', "004a"), charData('K', "004b"), charData('L', "004c"),
    charData('M', "004d"), charData('N', "004e"), charData('O', "004f"), charData('P', "0050"), charData('R', "0052"), charData('S', "0053"),
    charData('t', "0054"), charData('u', "0055"), charData('w', "0057"), charData('y', "0059"), charData('z', "005a"), 

    #Duże lietry polskie
    charData('Ą', "0104"), charData('Ć', "0106"), charData('Ę', "0118"), charData('Ł', "0141"), charData('Ń', "0143"), charData('Ó', "00d3"),
    charData('Ś', "015a"), charData('Ź', "0179"), charData('Ż', "017b"), 

    #Duże litery angielskie 
    #charData('q', "0051"), charData('v', "0056"), charData('x', "0058"),

    ]

#Ścieżki do folderów używanych przy trenowaniu, walidacji i testowaniu
base_dir = 'D:\\Progamowanie Python\\Uczenie Maszynowe\\datasetsGenerator\\datasets\\polish_lower_and_upper1'

train_dir = os.path.join(base_dir,'train')
if not os.path.exists(train_dir):
    os.mkdir(train_dir)

validation_dir = os.path.join(base_dir,'validation')
if not os.path.exists(validation_dir):
    os.mkdir(validation_dir)

test_dir = os.path.join(base_dir,'test')
if not os.path.exists(test_dir):
    os.mkdir(test_dir)


#Kopiowoanie danej liczby zdjęć do poszczególnych folderów
for char in charList:
    fnames = ['{}_{}.png'.format(char.unicode,i) for i in range(1,2000) ]
    for fname in fnames:
        src = os.path.join(base_dir,fname)
        dst = os.path.join(train_dir,char.unicode)
        if not os.path.exists(dst):
            os.mkdir(dst)
        dst = os.path.join(dst,fname)
        try:
            shutil.move(src,dst)
        except Exception:
            break

for char in charList:
    fnames = ['{}_{}.png'.format(char.unicode,i) for i in range(2000,2500) ]
    for fname in fnames:
        src = os.path.join(base_dir,fname)
        dst = os.path.join(validation_dir,char.unicode)
        if not os.path.exists(dst):
            os.mkdir(dst)
        dst = os.path.join(dst,fname)
        try:
            shutil.move(src,dst)
        except Exception:
            break

for char in charList:
    fnames = ['{}_{}.png'.format(char.unicode,i) for i in range(2500,3000) ]
    for fname in fnames:
        src = os.path.join(base_dir,fname)
        dst = os.path.join(test_dir,char.unicode)
        if not os.path.exists(dst):
            os.mkdir(dst)
        dst = os.path.join(dst,fname)
        try:
            shutil.move(src,dst)
        except Exception:
            break



#Generatory zwracające wszystkie pliki z danego foldera i jego podfolderów
#Podfolder jest traktowany jako odzielna etykeita
#Przeskalowane z 3 wymiarów (RGB) do 1 wymiaru 
train_datagen = ImageDataGenerator(
    rescale=1./255
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,target_size=(50,64),batch_size=64,class_mode='categorical'
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,target_size=(50,64),batch_size=64,class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,target_size=(50,64),batch_size=64,class_mode='categorical'
)


#Architektura sieci
model = models.Sequential()
model.add(layers.Conv2D(128,(3,3),activation='relu',input_shape=(50,64,3)))
model.add(layers.MaxPool2D((2,2)))
model.add(layers.Conv2D(256,(3,3),activation='relu'))
model.add(layers.MaxPool2D((2,2)))
model.add(layers.Conv2D(256,(3,3),activation='relu'))
model.add(layers.MaxPool2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(1024,activation='relu'))
model.add(layers.Dense(2,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])


history = model.fit_generator(
    train_generator,
    steps_per_epoch=40,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=50
)


#Wykresiki
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epchos = range(len(acc))

model.save('v1.h5')

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


