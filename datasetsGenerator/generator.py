import os
import fitz

booksDirName = "books"
datasetDirName = "datasets"
datasetOutputName = "gen1"

#charList = [
#    'a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó', 'p', 'r', 's', 'ś', 't', 'u', 'w', 'y', 'z', 'ź', 'ż',
#    'A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł', 'M', 'N', 'Ń', 'O', 'Ó', 'P', 'R', 'S', 'Ś', 'T', 'U', 'W', 'Y', 'Z', 'Ź', 'Ż'
#    ]

charList = [
    'a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó', 'p', 'r', 's', 'ś', 't', 'u', 'w', 'y', 'z', 'ź', 'ż',
    ]


dirPath = os.path.dirname(__file__) + "/"

amountOfBooks = 0
currentBookNumber = 0
currentBookPageCount = 0
currentPageNumber = 0

def getBooksPaths():
    booksDirPath = dirPath + booksDirName
    booksPaths = []

    for bookName in os.listdir(booksDirPath):
        bookPath = booksDirPath + "/" + bookName
        if os.path.isfile(bookPath):
            if bookPath.endswith(".pdf"):
                booksPaths.append(bookPath)

    return booksPaths

def createBookDataset(bookPath):
    global currentBookPageCount
    global currentPageNumber

    book = fitz.open(bookPath)

    if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber)):
        os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber))

    currentBookPageCount = book.pageCount
    for page in book:
        currentPageNumber += 1

        if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/p" + str(currentPageNumber)):
            os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/p" + str(currentPageNumber))

        generationLoadingBar()
        createPageDataset(page)
    
def createPageDataset(page):
    for char in charList:
        if not os.path.exists(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/p" + str(currentPageNumber) + "/" + char):
            os.makedirs(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/p" + str(currentPageNumber) + "/" + char)
        
        generateCharDataset(char, page.searchFor(char, 1000), page)

def generateCharDataset(char, areas, page):
    i = 0
    for area in areas:
        i += 1
        iarea = area.irect
        mat = fitz.Matrix(4, 4)
        img = page.getPixmap(matrix = mat, clip = iarea)
        img.writeImage(dirPath + datasetDirName + "/" + datasetOutputName + "/book" + str(currentBookNumber) + "/p" + str(currentPageNumber) + "/" + char + "/" + str(i) + ".png")

def generationLoadingBar():
    global amountOfBooks
    global currentBookNumber
    global currentBookPageCount
    global currentPageNumber

    barLength = 50

    percentDone = (currentPageNumber / currentBookPageCount) * 100
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

        for bookPath in booksPaths:
            currentBookNumber += 1
            createBookDataset(bookPath)

        print("Finished")
    else:
        print("No books found")


if __name__ == "__main__":
    main()



