import mysql.connector
from os import listdir
from os.path import isfile, join

class charData:
    def __init__(self, char, unicode):
        self.char = char
        self.unicode = unicode

charList = [

    #Małe lietry
    charData('a', "0061"), charData('b', "0062"), charData('c', "0063"), charData('d', "0064"), charData('e', "0065"), charData('f', "0066"), charData('g', "0067"), charData('h', "0068"), charData('i', "0069"), charData('j', "006a"), charData('k', "006b"), charData('l', "006c"), charData('m', "006d"), charData('n', "006e"), charData('o', "006f"), charData('p', "0070"), charData('r', "0072"), charData('s', "0073"), charData('t', "0074"), charData('u', "0075"), charData('w', "0077"), charData('y', "0079"), charData('z', "007a"), 

    #Małe lietry polskie
    charData('ą', "0105"), charData('ć', "0107"), charData('ę', "0119"), charData('ł', "0142"), charData('ń', "0144"), charData('ó', "00f3"), charData('ś', "015b"), charData('ź', "017a"), charData('ż', "017c"), 

    #Duże litery
    charData('A', "0041"), charData('B', "0042"), charData('C', "0043"), charData('D', "0044"), charData('E', "0045"), charData('F', "0046"), charData('G', "0047"), charData('H', "0048"), charData('I', "0049"), charData('J', "004a"), charData('K', "004b"), charData('L', "004c"), charData('M', "004d"), charData('N', "004e"), charData('O', "004f"), charData('P', "0050"), charData('R', "0052"), charData('S', "0053"), charData('T', "0054"), charData('U', "0055"), charData('W', "0057"), charData('Y', "0059"), charData('Z', "005a"), 

    #Duże lietry polskie
    charData('Ą', "0104"), charData('Ć', "0106"), charData('Ę', "0118"), charData('Ł', "0141"), charData('Ń', "0143"), charData('Ó', "00d3"), charData('Ś', "015a"), charData('Ź', "0179"), charData('Ż', "017b"), 

    #Liczby
    charData('0', "0030"), charData('1', "0031"), charData('2', "0032"), charData('3', "0033"), charData('4', "0034"), charData('5', "0035"), charData('6', "0036"), charData('7', "0037"), charData('8', "0038"), charData('9', "0039"),

    #Inne znaki 
    charData('!', "0021"), charData('?', "003f"), charData(',', "002c"), charData('.', "002e"), charData('(', "0028"), charData(')', "0029"), charData(':', "003a"), charData('-', "002d"), 
    
    #Inne znaki rzadkie
    charData('+', "002b"), charData('=', "003d"), charData('*', "002a"), charData('/', "002f"), charData(';', "003b"),

    #Inne znaki polskie
    charData('”', "201d"), charData('„', "201e"), 

    ]

def connectToDatabase():
    return mysql.connector.connect(
        host="localhost",
        user="tfs",
        password="3sHUCwk3)%$%?Q5U",
        database="baza_do_nauki"
    )

def getCursor(db):
    return db.cursor()

def insertLetters(db, cur):

    sql = "INSERT INTO litery (litera_id, znak) VALUES (%s, %s)"
    for char in charList:
        val = (char.unicode, char.char)
        cur.execute(sql, val)
        print("Letter: " + char.char + " inserted")

    db.commit()

def insertChars(db, cur):
    folderName = "polish_1_hd"
    folderPath = "/var/lib/tfs/training/datasets/" + folderName + "/"

    fileNames = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

    sql = "INSERT INTO znaki (litera_id, sciezka) VALUES (%s, %s)"


    i = 0
    for fileName in fileNames:
        val = (fileName[:4], folderPath + fileName)
        cur.execute(sql, val)
        i += 1
        print("Char: " + str(i) + " inserted")

    db.commit()


def main():
    db = connectToDatabase()
    cur = getCursor(db)
    #insertLetters(db, cur) DONE
    insertChars(db, cur)



if __name__ == "__main__":
    main()