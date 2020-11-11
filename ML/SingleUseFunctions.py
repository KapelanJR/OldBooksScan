import mysql.connector
import os

def append_ext(fn):
    return fn+".jpg"


#Create CSV labels from paths
#Path tuple
def create_CSV(path,dst):
    with open(dst,'w') as f:
        f.write("id,label\n")
        for i,fname in enumerate(path):
            fil = fname
            fil = os.path.basename(os.path.normpath(fil))
            f.write("{},{}\n".format(fil.replace('.jpg',''),fil[0:4]))


def get_Data(images,sftp,dest):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dest = os.path.join(dir_path,dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    for image in images:
        fname = os.path.basename(os.path.normpath(image[0]))
        if not os.path.exists(os.path.join(dest,fname)):
            sftp.get(image[0],os.path.join(dest,fname))


#Function used to connect to database
def database_connection(host,user,password,database):
    mydb = mysql.connector.connect(
    host= host,
    user= user,
    password=password,
    database=database
    )
    return mydb.cursor()

#Klasa posiadająca dane o danym znaku
class charData:
    def __init__(self, char, unicode):
        self.char = char
        self.unicode = unicode
        self.count = 0


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
    charData('+', "002b"), charData('=', "003d"), charData('/', "002f"), charData(';', "003b"),

    #Inne znaki bardzo rzadkie
    #charData('%', "0025"), charData('^', "005e"), charData('$', "0024"), charData('&', "0026"), charData('#', "0023"), charData('<', "003c"), charData('>', "003e"), charData('\\', "003e"), charData('*', "002a")

    #Inne znaki polskie
    charData('”', "201d"), charData('„', "201e"), 

    #Inne znaki angielskie
    #charData('"', "0022"), charData('\'', "0027")
    ]


def MakeSets(train_dir,test_dir,validation_dir,base_dir,charList):

    for char in charList:
        fnames = ['{}_{}.jpg'.format(char.unicode,i) for i in range(1,3001)]
        for fname in fnames:
            dst = os.path.join(base_dir,fname)
            if(os.path.exists(dst)):
                char.count +=1
            else:
                continue


    #Kopiowoanie danej liczby zdjęć do poszczególnych folderów
    current_index = 1
    current_count = 0
    for char in charList:
        fnames = []
        while(current_count < int((0.75*char.count))):
            path = os.path.join(base_dir,'{}_{}.jpg'.format(char.unicode,current_index))
            if(os.path.exists(path)):
                fnames.append('{}_{}.jpg'.format(char.unicode,current_index))
                current_count += 1
            current_index += 1
        current_count = 0
        current_index = 1
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(train_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                continue

    current_index = 1
    current_count = 0
    for char in charList:
        fnames = []
        while(current_count < int((0.9*char.count))):
            path = os.path.join(base_dir,'{}_{}.jpg'.format(char.unicode,current_index))
            if(os.path.exists(path)):
                current_count += 1
                if(current_count > int((0.75*char.count))):
                    fnames.append('{}_{}.jpg'.format(char.unicode,current_index))
            current_index += 1
        current_count = 0
        current_index = 1
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(validation_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                continue

    current_index = 1
    current_count = 0
    for char in charList:
        fnames = []
        while(current_count < int((0.99*char.count))):
            path = os.path.join(base_dir,'{}_{}.jpg'.format(char.unicode,current_index))
            if(os.path.exists(path)):
                current_count += 1
                if(current_count > int((0.9*char.count))):
                    fnames.append('{}_{}.jpg'.format(char.unicode,current_index))
            current_index += 1
        current_count = 0
        current_index = 1
        for fname in fnames:
            src = os.path.join(base_dir,fname)
            dst = os.path.join(test_dir,char.unicode)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst = os.path.join(dst,fname)
            try:
                shutil.copyfile(src,dst)
            except Exception:
                continue