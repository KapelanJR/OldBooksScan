from PIL import Image
import numpy as np
from scipy import ndimage
import os
import threading

#Ustawienia folderów
inputDirName = "test"
outputDirName = "test"
inputsDirName = "input"
outputsDirName = "output"

#Ustawienia wykrywania, dane są podawane w procentach, 1 = 100%
contrastDivThreshold = "auto" #Dzielnik kontrastu, "auto" - jeśli ma być automatyczny
edgesDetectionThreshold = 0.45 #Ile procent lini ma być czarne aby wykryło, że linia ta jest na końcach zdjęcia (a nie jest tekstem) i ma zostać ustawić na kolor biały 
dirtDetectionThreshold = 0.975 #Ile procent lini ma być białe, aby wykryło, że ewentualne czarne częsci nie są tekstem, a jedynie jakimś brudem
edgesDetectionOffset = 0.05 #Ile procent lini ma dodatkwo zostać zamienione na białe pomiędzy wykrytymi końcami a tekstem
minTextLineHeight = 0.005 #Minimalna wysokość lini w procentach
maxTextLineHeight = 0.06 #Maksymalna wysokość lini w procentach
minCharWidth = 0.003 #Minimalna szerokość znaku
maxCharWidth = 0.06 #Maksymalna szerokość znaku
minSpaceWidth = 0.008 #Minimalna szerokość spacji

#Definicja ścieżki bezwzględnej
dirPath = os.path.dirname(__file__)

def devideContrast(pixels):
    imgHeight, imgWidth = pixels.shape

    if contrastDivThreshold == "auto": 
        colorAvg = int(np.average(pixels[int(imgHeight * 0.4):int(imgHeight * 0.6), int(imgWidth * 0.4):int(imgWidth * 0.6)]))
        return np.where(pixels > colorAvg - int(colorAvg * 0.3), 1, 0)
    else:
        return np.where(pixels > int(contrastDivThreshold * 255), 1, 0)

def removeEdges(pixels):
    imgHeight, imgWidth = pixels.shape

    heightOffset = int(edgesDetectionOffset * imgHeight)
    widthOffset = int(edgesDetectionOffset * imgWidth)

    #Góra
    offsetCounter = 0
    edgeFlag = False
    for i in range(0, int(imgHeight/2), 1):
        rowAvg = np.average(pixels[i])
        if rowAvg >= dirtDetectionThreshold:
            pixels[i].fill(1)
            if edgeFlag == True: offsetCounter += 1
        elif rowAvg < (1 - edgesDetectionThreshold):
            pixels[i].fill(1)
            edgeFlag = True
        else: 
            if edgeFlag == True: offsetCounter += 1
        if (offsetCounter == heightOffset):
            if i <= heightOffset: pixels[0:i].fill(1)
            else: pixels[i-heightOffset:i].fill(1)
    
    #Dół
    offsetCounter = 0
    edgeFlag = False
    for i in range(imgHeight-1, int(imgHeight/2), -1):
        rowAvg = np.average(pixels[i])
        if rowAvg >= dirtDetectionThreshold:
            pixels[i].fill(1)
            if edgeFlag == True: offsetCounter += 1
        elif rowAvg < (1 - edgesDetectionThreshold):
            pixels[i].fill(1)
            edgeFlag = True
        else:
            if edgeFlag == True: offsetCounter += 1
        if (offsetCounter == heightOffset):
            if (imgHeight-1 - i) <= heightOffset: pixels[i:imgHeight-1].fill(1)
            else: pixels[i:i+heightOffset].fill(1)
    
    #Lewo
    offsetCounter = 0
    edgeFlag = False
    for i in range(0, int(imgWidth/2), 1):
        rowAvg = np.average(pixels[:, i])
        if rowAvg >= dirtDetectionThreshold:
            pixels[:, i].fill(1)
            if edgeFlag == True: offsetCounter += 1
        elif rowAvg < (1 - edgesDetectionThreshold):
            pixels[:, i].fill(1)
            edgeFlag = True
        else:
            if edgeFlag == True: offsetCounter += 1
        if (offsetCounter == widthOffset):
            if i <= widthOffset: pixels[:, 0:i].fill(1)
            else: pixels[:, i-widthOffset:i].fill(1)

    #Prawo
    offsetCounter = 0
    edgeFlag = False
    for i in range(imgWidth-1, int(imgWidth/2), -1):
        rowAvg = np.average(pixels[:, i])
        if rowAvg >= dirtDetectionThreshold:
            pixels[:, i].fill(1)
            if edgeFlag == True: offsetCounter += 1
        elif rowAvg < (1 - edgesDetectionThreshold):
            pixels[:, i].fill(1)
            edgeFlag = True
        else:
            if edgeFlag == True: offsetCounter += 1
        if (offsetCounter == widthOffset):
            if (imgWidth-1 - i) <= widthOffset: pixels[:, i:imgWidth-1].fill(1)
            else: pixels[:, i:i+widthOffset].fill(1)
                
    return pixels

def countWhitePixelsRows(pixels):
    imgHeight, imgWidth = pixels.shape
    return imgHeight - np.count_nonzero(imgWidth - np.count_nonzero(pixels, axis=1))

def detectCorrectRotation(pixels, orgPixels):
    rowsMaxCount = countWhitePixelsRows(pixels)
    rowsMaxAngle = 0
    for currentAngle in np.arange(-3, 3, 1/3):
        pixelsTest = ndimage.rotate(pixels, currentAngle, reshape=False, mode="constant", cval=1, prefilter=False)
        rowsCurrentCount = countWhitePixelsRows(pixelsTest)
        if rowsCurrentCount > rowsMaxCount:
            rowsMaxCount = rowsCurrentCount
            rowsMaxAngle = currentAngle

    pixels = ndimage.rotate(pixels, rowsMaxAngle, reshape=False, mode="constant", cval=1, prefilter=False)
    orgPixels = ndimage.rotate(orgPixels, rowsMaxAngle, reshape=False, mode="constant", cval=1, prefilter=False)
    
    return pixels, orgPixels

def cleanPixels(orgPixels):
    pixels = devideContrast(orgPixels)
    pixels = removeEdges(pixels)
    pixels, orgPixels = detectCorrectRotation(pixels, orgPixels)
    
    return pixels, orgPixels

def detectTextLines(pixels):
    imgHeight, _ = pixels.shape
    textLines = []
    textRows = np.where(np.any(pixels == 0, axis=1))
    lastRow = -1
    for row in textRows[0]:
        if row - lastRow == 1: textLines[len(textLines)-1].append(row)
        else: textLines.append([row])
        lastRow = row

    i = 0
    while i < len(textLines):
        if len(textLines[i]) < int(imgHeight * minTextLineHeight) or len(textLines[i]) > int(imgHeight * maxTextLineHeight): del textLines[i] 
        else: i += 1


    return textLines

def detectCharsInLines(textLines, pixels, orgPixels):

    '''

    Struktura listy "chars":
        chars -> linie | 
                       |-> linia | ,                           wyrazy |
                                 |-> indeksy wierszy pikseli          |-> znaki |
                                                                                |-> znak |
                                                                                         |-> indeksy kolumn pikseli
    
    Pierwszy wymiar wskazuje na daną linie tekstu
    Drugi na indeksy wierszy danej lini ([0]) lub na zbiór znaków ([1]) 
    Trzeci w przypadku indeksów lini wskazuje na indeks danego pikselowego wiersza, w przypadku znaków wskazuje na dany znak
    Czwarty wstępuje tylko dla znaków i wskazuje na indeks danej pikselowej kolumny

               kolumny
       wiersze 5 6 7 8 9
            21 # # # #
            22 #       #
            23 #       #
            24 # # # #                  
            25 #       #
            26 #       #
            27 # # # #

    '''
    imgHeight, imgWidth = pixels.shape

    #Odnajdź lokalizacje prostokąta w którym znajduje się cały tekst
    crop1a = np.argmax(pixels == 0, axis=1)
    crop1i = np.min(crop1a[np.nonzero(crop1a)])
    crop2a = np.argmax(np.flip(pixels, axis=1) == 0, axis=1)
    crop2i = imgWidth - np.min(crop2a[np.nonzero(crop2a)])
    crop3a = np.argmax(pixels == 0, axis=0)
    crop3i = np.min(crop3a[np.nonzero(crop3a)])
    crop4a = np.argmax(np.flip(pixels, axis=0) == 0, axis=0)
    crop4i = imgHeight - np.min(crop4a[np.nonzero(crop4a)])

    #Wytnij odnaleziony prostokąt i wylicz dla niego próg kontrastu
    cropOrgPixels = np.zeros(orgPixels.shape, dtype="uint8") + 255
    cropOrgPixels[crop3i:crop4i, crop1i:crop2i] = orgPixels[crop3i:crop4i, crop1i:crop2i]
    cropOrgPixels = np.where(cropOrgPixels > np.average(cropOrgPixels[crop3i:crop4i, crop1i:crop2i]) - int(np.average(cropOrgPixels[crop3i:crop4i, crop1i:crop2i]) * 0.10), 1, 0)

    #Dla każdej linii wyszukaj kolumny pikseli z czarnymi pikselami, a następnie podziel je na wyrazy i znaki. Operuj na wyciętym wcześniej prostokącie.
    chars = []
    for line in textLines:
        chars.append([line, []])
        charsInLine = [[[]]]
        textColumns = np.where(np.any(cropOrgPixels[line] == 0, axis=0))
        lastColumn = -1
        
        #Wyszukaj kolumny, podziel je na wyrazy i znaki
        for column in textColumns[0]:
            words_i = len(charsInLine)-1
            char_i = len(charsInLine[words_i])-1
            if column - lastColumn == 1: charsInLine[words_i][char_i].append(column)
            elif column - lastColumn > 1 and column - lastColumn < int(minSpaceWidth * imgWidth): charsInLine[words_i].append([column])
            else: charsInLine.append([[column]])
            lastColumn = column

        #Oczyść wynik z zbyt krótkich znaków i pustych wyrazów
        i = 0
        while i < len(charsInLine):
            j = 0
            while j < len(charsInLine[i]):
                if len(charsInLine[i][j]) < int(imgWidth * minCharWidth) or len(charsInLine[i][j]) > int(imgWidth * maxCharWidth): del charsInLine[i][j]
                else: j += 1
            if len(charsInLine[i]) == 0: del charsInLine[i]
            else: i += 1

        #Zapisz wynik do listy "chars"
        line_i = len(chars)-1
        for charsInWord in charsInLine:
            chars[line_i][1].append([])
            words_i = len(chars[line_i][1])-1
            for char in charsInWord:
                chars[line_i][1][words_i].append(char)
                
    return chars

def detectChars(pixels, opixels):
    textLines = detectTextLines(pixels)
    chars = detectCharsInLines(textLines, pixels, opixels)
    
    return chars

def getChars(bookName, bookNum, page, pageNum):
    img = Image.open(dirPath + "/" + inputsDirName + "/" + inputDirName + "/" + bookName + "/" + page).convert('L')
    orgPixels = np.array(img, dtype="uint8")
    pixels, orgPixels = cleanPixels(orgPixels)
    chars = detectChars(pixels, orgPixels)

    for line_i in range(len(chars)):
        for word_i in range(len(chars[line_i][1])):
            for char_i in range(len(chars[line_i][1][word_i])):
                dirToSave = dirPath + "/" + outputsDirName + "/" + outputDirName + "/" + str(bookNum+1) + "/" + str(pageNum+1) + "/" + str(line_i+1) + "/" + str(word_i+1) + "/chars"
                if not os.path.exists(dirToSave): os.makedirs(dirToSave)
                charPixels = orgPixels[chars[line_i][0]][:, chars[line_i][1][word_i][char_i]]
                Image.fromarray(charPixels).save(dirToSave + "/" + str(char_i+1) + ".jpg")

def scanPages(bookName, bookNum):
    pages = os.listdir(dirPath + "/" + inputsDirName + "/" + inputDirName + "/" + bookName)

    threads = []
    for page_i in range(len(pages)):
        t = threading.Thread(target=getChars, args=[bookName, bookNum, pages[page_i], page_i])
        t.start()
        threads.append(t)

    for t in threads: t.join()


def scanBooks():
    booksNames = next(os.walk(dirPath + "/" + inputsDirName + "/" + inputDirName))[1]
    for book_i in range(len(booksNames)):
        print("Scanning book: " + booksNames[book_i])
        scanPages(booksNames[book_i], book_i)

def main():
    scanBooks()
    print("Finished")

if __name__ == "__main__":
    main()