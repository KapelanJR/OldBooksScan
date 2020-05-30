import os
import fitz

#Ustawienia
booksDirName = "books"
datasetDirName = "datasets"
datasetOutputName = "gen1"
defaultCharLimit = 200
pageOffset = 10

#Klasa posiadająca dane o danym znaku
class charData:
    def __init__(self, char, charLimit = defaultCharLimit):
        self.char = char
        self.charLimit = charLimit
        self.count = 0

#Lista znaków
charList = [
    charData('a'), charData('ą'), charData('b'), charData('c'), charData('ć'), charData('d'), charData('e'), charData('ę'), charData('f'), charData('g'), 
    charData('h'), charData('i'), charData('j'), charData('k'), charData('l'), charData('ł'), charData('m'), charData('n'), charData('ń'), charData('o'), 
    charData('ó'), charData('p'), charData('r'), charData('s'), charData('ś'), charData('t'), charData('u'), charData('w'), charData('y'), charData('z'), 
    charData('ź'), charData('ż')
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

#Utwórz folder dla każdej książki i iteruj przez jej strony
def createBookDataset(bookPath):
    global currentBookPageCount
    global currentPageNumber

    book = fitz.open(bookPath)

    if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber)):
        os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber))

    currentBookPageCount = book.pageCount
    currentPageNumber = 0

    for i in range(pageOffset + 1, currentBookPageCount - pageOffset):
        currentPageNumber += 1
        generationLoadingBar()
        createPageDataset(book[i])

#Utwórz folder dla każdego znaku i wyszukaj ich występowania na danej stronie
def createPageDataset(page):
    for charData in charList:
        if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/" + charData.char):
            os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/" + charData.char)
        
        generateCharDataset(charData, page.searchFor(charData.char, 1000), page)

#Zapisz znalezione fragmenty renderu PDF z danym szukanym znakiem jako obrazki PNG, każdy następny obrazek (danego znaku) ma nazwę o 1 większą niż poprzedni
def generateCharDataset(charData, areas, page):
    for area in areas:
        if charData.count < charData.charLimit:
            charData.count += 1
            img = page.getPixmap(matrix = fitz.Matrix(4, 4), clip = area.irect)
            img.writeImage(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/" + charData.char + "/" + str(charData.count) + ".png")

#Po wygenerowaniu zbioru danych dla danej książki, wyczyść licznik występowania danego znaku
def clearCharsCount():
    for charData in charList:
        charData.count = 0

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
            clearCharsCount()

        print("Finished")
    else:
        print("No books found")


if __name__ == "__main__":
    main()



