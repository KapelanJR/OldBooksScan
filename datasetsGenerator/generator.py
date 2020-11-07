import os
import fitz

#Ustawienia
booksDirName = "books"
datasetDirName = "datasets"
datasetOutputName = "polish_1_hd"
defaultCharAllLimit = 3000
defaultCharBookLimit = 35
pageOffset = 12

#Klasa posiadająca dane o danym znaku
class charData:
    def __init__(self, char, unicode, charAllLimit = defaultCharAllLimit, charBookLimit = defaultCharBookLimit):
        self.char = char
        self.unicode = unicode
        self.charAllLimit = charAllLimit
        self.charBookLimit = charBookLimit
        self.countBook = 0
        self.countAll = 0

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
    charData('+', "002b", charBookLimit=1000), charData('=', "003d", charBookLimit=1000), charData('/', "002f", charBookLimit=1000), charData(';', "003b", charBookLimit=1000),

    #Inne znaki bardzo rzadkie
    #charData('%', "0025"), charData('^', "005e"), charData('$', "0024"), charData('&', "0026"), charData('#', "0023"), charData('<', "003c"), charData('>', "003e"), charData('\\', "003e"), charData('*', "002a")

    #Inne znaki polskie
    charData('”', "201d"), charData('„', "201e"), 

    #Inne znaki angielskie
    #charData('"', "0022"), charData('\'', "0027")

    #Spacja
    charData(' ', "0020"),

    ]


#Definicja ścieżki bezwzględnej
dirPath = os.path.dirname(__file__) + "/"

#Definicja zmiennych globalnych
amountOfBooks = 0
currentBookNumber = 0
currentBookPageCount = 0
currentPageNumber = 0

#Pobierz ścieżki książek (pdf) i zapisz je w liście "booksPaths"
def getBooksPaths():
    booksDirPath = dirPath + booksDirName
    booksPaths = []

    for bookName in os.listdir(booksDirPath):
        bookPath = booksDirPath + "/" + bookName
        if os.path.isfile(bookPath):
            if bookPath.endswith(".pdf"):
                booksPaths.append(bookPath)

    return booksPaths

#Iteruj przez strony każdej książki
def createBookDataset(bookPath):
    global currentBookPageCount
    global currentPageNumber

    book = fitz.open(bookPath)

    currentBookPageCount = book.pageCount
    currentPageNumber = 0

    for i in range(pageOffset + 1, currentBookPageCount - pageOffset):
        currentPageNumber += 1
        generationLoadingBar()
        createPageDataset(book[i])

#Wyszukaj występowanie danego znaku w książce
def createPageDataset(page):
    textBlocks = page.getText("rawdict", flags=fitz.TEXT_PRESERVE_LIGATURES + fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    for charData in charList:
        generateCharDataset(charData, searchForCaseSensitive(textBlocks, charData.char), page)

#Zapisz znalezione fragmenty renderu PDF z danym szukanym znakiem jako obrazki PNG, każdy następny obrazek (danego znaku) ma nazwę o 1 większą niż poprzedni
def generateCharDataset(charData, areas, page):
    for area in areas:
        if charData.countAll < charData.charAllLimit and charData.countBook < charData.charBookLimit:
            charData.countBook += 1
            charData.countAll += 1
            img = page.getPixmap(matrix = fitz.Matrix(8, 8), clip = area.irect)
            if not all(v == 0 for v in img.irect[:4]):
                img.writeImage(dirPath + datasetDirName + "/" + datasetOutputName + "/" + charData.unicode + "_" + str(charData.countAll) + ".jpg")
            

#Po wygenerowaniu zbioru danych dla danej książki, wyczyść licznik występowania danego znaku
def clearCharsCountBook():
    for charData in charList:
        charData.countBook = 0

#Funkcja do wyszukiwania znaków i zwracania ich lokalizacji na stronie
def searchForCaseSensitive(textBlocks, charToSearch):
    areas = []
    for textBlock in textBlocks:
        lines = textBlock["lines"]
        for line in lines:
            spans = line["spans"]
            for span in spans:
                chars = span["chars"]
                for char in chars:
                    if char["c"] == charToSearch:
                        areas.append(fitz.Rect(char["bbox"][:4]))
    
    return areas

#Rysuj ładny pasek postępu
def generationLoadingBar():
    global amountOfBooks
    global currentBookNumber
    global currentBookPageCount
    global currentPageNumber

    barLength = 50

    percentDone = (currentPageNumber / (currentBookPageCount - pageOffset - pageOffset - 1)) * 100
    barDone = int((barLength / 100) * percentDone)

    print("Book", currentBookNumber, "from", amountOfBooks, "generation progress: ", end="")
    print("[", end="")
    for _ in range(barDone):
        print("█", end="")
    for _ in range(barLength - barDone):
        print(" ", end="")
    print("] ", end="")
    print(int(percentDone), end="")
    print("%", end="\r")
    
    if barDone == barLength:
        print(end="\n")

def main():
    global currentBookNumber
    global amountOfBooks

    booksPaths = getBooksPaths()
  
    if len(booksPaths) > 0:
        amountOfBooks = len(booksPaths)

        if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName):
            os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName)

        #Iteruj po ksiązkach
        for bookPath in booksPaths:
            currentBookNumber += 1
            createBookDataset(bookPath)
            clearCharsCountBook()

        print("Finished")
    else:
        print("No books found")

if __name__ == "__main__":
    main()