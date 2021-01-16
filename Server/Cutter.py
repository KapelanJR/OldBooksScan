from PIL import Image
import numpy as np
from scipy import ndimage
import os
import threading
import sys
import mysql.connector
import fitz

#Ustawienia folderów
inputsDirName = "/var/lib/tfs/PDFs_pages"
outputsDirName = "/var/lib/tfs/PDFs_letters"
PDFFileDirName = "/var/lib/tfs/PDFs_toScan"

#Ustawienia wykrywania, dane są podawane w procentach, 1 = 100%
contrastDivThreshold = "auto" #Dzielnik kontrastu, "auto" - jeśli ma być automatyczny
edgesDetectionThreshold = 0.45 #Ile procent lini ma być czarne aby wykryło, że linia ta jest na końcach zdjęcia (a nie jest tekstem) i ma zostać ustawić na kolor biały 
dirtDetectionThreshold = 0.975 #Ile procent lini ma być białe, aby wykryło, że ewentualne czarne częsci nie są tekstem, a jedynie jakimś brudem
edgesDetectionOffset = 0.05 #Ile procent lini ma dodatkwo zostać zamienione na białe pomiędzy wykrytymi końcami a tekstem
minTextLineHeight = 0.005 #Minimalna wysokość lini w procentach
maxTextLineHeight = 0.06 #Maksymalna wysokość lini w procentach
minCharWidth = 0.003 #Minimalna szerokość znaku
maxCharWidth = 0.06 #Maksymalna szerokość znaku
maxCharAvgColor = 0.5 #Ile maksymalnie procent znaku może być czarne
minSpaceWidth = 0.008 #Minimalna szerokość spacji
whiteColumnsToAdd = 0.002 #Liczba białych kolumn do dodania pomiędzy znakami w procentach 

multithreadedScanning = True
maxThreadCount = 10 #Maksymalna liczba jednocześnie działających wątków

showPrints = False

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
    for currentAngle in np.arange(-3, 3, 1/2):
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
    textLines = [[]]
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
    chars = []

    #Odnajdź lokalizacje prostokąta w którym znajduje się cały tekst
    crop1a = np.argmax(pixels == 0, axis=1)
    if not np.any(crop1a): return chars
    crop1i = np.min(crop1a[np.nonzero(crop1a)])
    crop2a = np.argmax(np.flip(pixels, axis=1) == 0, axis=1)
    if not np.any(crop2a): return chars
    crop2i = imgWidth - np.min(crop2a[np.nonzero(crop2a)])
    crop3a = np.argmax(pixels == 0, axis=0)
    if not np.any(crop3a): return chars
    crop3i = np.min(crop3a[np.nonzero(crop3a)])
    crop4a = np.argmax(np.flip(pixels, axis=0) == 0, axis=0)
    if not np.any(crop4a): return chars
    crop4i = imgHeight - np.min(crop4a[np.nonzero(crop4a)])

    #Wytnij odnaleziony prostokąt i wylicz dla niego próg kontrastu
    cropOrgPixels = np.zeros(orgPixels.shape, dtype="uint8") + 255
    cropOrgPixels[crop3i:crop4i, crop1i:crop2i] = orgPixels[crop3i:crop4i, crop1i:crop2i]
    cropOrgPixels = np.where(cropOrgPixels > np.average(cropOrgPixels[crop3i:crop4i, crop1i:crop2i]) - int(np.average(cropOrgPixels[crop3i:crop4i, crop1i:crop2i]) * 0.10), 1, 0)

    #Dla każdej linii wyszukaj kolumny pikseli z czarnymi pikselami, a następnie podziel je na wyrazy i znaki. Operuj na wyciętym wcześniej prostokącie.
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

        #Oczyść wynik z zbyt krótkich znaków, zbyt długich znaków, zbyt ciemnych znaków i pustych wyrazów
        i = 0
        while i < len(charsInLine):
            j = 0
            while j < len(charsInLine[i]):
                charAvgColor = 0
                charPixels = cropOrgPixels[line][:, charsInLine[i][j]]
                if not charPixels.size == 0: charAvgColor = np.average(cropOrgPixels[line][:, charsInLine[i][j]])
                if len(charsInLine[i][j]) < int(imgWidth * minCharWidth) or len(charsInLine[i][j]) > int(imgWidth * maxCharWidth) or charAvgColor < (1 - maxCharAvgColor): del charsInLine[i][j]
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
    if not textLines: return []
    chars = detectCharsInLines(textLines, pixels, opixels)
    return chars

def getCharPixels(orgPixels, chars, line_i, word_i, char_i):
    _, imgWidth = orgPixels.shape
    h = chars[line_i][0]
    w = chars[line_i][1][word_i][char_i]
    charPixels = orgPixels[h][:, w]

    if imgWidth > 1000:
        if chars[line_i][1][word_i][char_i][0] > 1:
            columnToAddBeginning = orgPixels[h, w[0]-2].reshape(-1, 1)
            for _ in range(0, int(whiteColumnsToAdd * imgWidth)): charPixels = np.concatenate((columnToAddBeginning, charPixels), axis=1)
        if chars[line_i][1][word_i][char_i][-1] < imgWidth-2:
            columnToAddEnd = orgPixels[h, w[-1]+2].reshape(-1, 1)
            for _ in range(0, int(whiteColumnsToAdd * imgWidth)): charPixels = np.concatenate((charPixels, columnToAddEnd), axis=1)
    else:
        if chars[line_i][1][word_i][char_i][0] > 0:
            columnToAddBeginning = orgPixels[h, w[0]-1].reshape(-1, 1)
            for _ in range(0, int(whiteColumnsToAdd * imgWidth)): charPixels = np.concatenate((columnToAddBeginning, charPixels), axis=1)
        if chars[line_i][1][word_i][char_i][-1] < imgWidth-1:
            columnToAddEnd = orgPixels[h, w[-1]+1].reshape(-1, 1)
            for _ in range(0, int(whiteColumnsToAdd * imgWidth)): charPixels = np.concatenate((charPixels, columnToAddEnd), axis=1)

    return charPixels

def getChars(bookName, bookID, page, pageNum):
    img = Image.open(inputsDirName + "/" + bookName + "/" + page).convert('L')
    orgPixels = np.array(img, dtype="uint8")
    pixels, orgPixels = cleanPixels(orgPixels)
    chars = detectChars(pixels, orgPixels)

    db = mysql.connector.connect(host="localhost", user="tfs", password="3sHUCwk3)%$%?Q5U", database="baza_wynikowa")
    cur = db.cursor()

    cur.execute("INSERT INTO strony (ksiazka_id, numer_strony, sciezka) VALUES (%s, %s, %s)", (bookID, os.path.splitext(page)[0], inputsDirName + "/" + bookName + "/" + page))
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    pageID = int(cur.fetchone()[0])

    if chars:
        for line_i in range(len(chars)):
            cur.execute("INSERT INTO linie (strona_id, numer_linii) VALUES (%s, %s)", (pageID, line_i+1))
            db.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            lineID = int(cur.fetchone()[0])
            for word_i in range(len(chars[line_i][1])):
                cur.execute("INSERT INTO wyrazy (linia_id, numer_wyrazu) VALUES (%s, %s)", (lineID, word_i+1))
                db.commit()
                cur.execute("SELECT LAST_INSERT_ID()")
                wordID = int(cur.fetchone()[0])
                for char_i in range(len(chars[line_i][1][word_i])):
                    dirToSave = outputsDirName + "/" + str(bookID) + "/" + str(pageNum+1) + "/" + str(line_i+1) + "/" + str(word_i+1)
                    if not os.path.exists(dirToSave): os.makedirs(dirToSave)
                    charPixels = getCharPixels(orgPixels, chars, line_i, word_i, char_i)
                    imagePath = dirToSave + "/" + str(char_i+1) + ".jpg"
                    Image.fromarray(charPixels).save(imagePath)
                    x1 = int(chars[line_i][1][word_i][char_i][0])
                    y1 = int(chars[line_i][0][0])
                    x2 = int(chars[line_i][1][word_i][char_i][-1])
                    y2 = int(chars[line_i][0][-1])
                    cur.execute("INSERT INTO litery (wyraz_id, numer_litery, x1, y1, x2, y2, sciezka) VALUES (%s, %s, %s, %s, %s, %s, %s)", (wordID, char_i+1, x1, y1, x2, y2, imagePath))
                    db.commit()

    db.close()
    if showPrints: print("  Page " + str(pageNum+1) + " done" )

def scanPages(bookName, bookID):
    pages = os.listdir(inputsDirName + "/" + bookName)

    if multithreadedScanning:
        for i in range(0, len(pages), maxThreadCount):
            threads = []
            tc = maxThreadCount
            if len(pages[i:]) < 10: tc = len(pages[i:])

            for page_i in range(i, i+tc):
                t = threading.Thread(target = getChars, args = [bookName, bookID, pages[page_i], page_i])
                threads.append(t)

            for t in threads: t.start()
            for t in threads: t.join()
    else:
        for page_i in range(len(pages)): getChars(bookName, bookID, pages[page_i], page_i)

def convertPDFPagesToJPG(bookName, bookID):
    book = fitz.open(PDFFileDirName + "/" + bookName + ".pdf")
    dirToSave = inputsDirName + "/" + bookName
    if not os.path.exists(dirToSave): os.makedirs(dirToSave)
    for page in book: page.getPixmap(matrix=fitz.Matrix(8, 8)).writeImage(dirToSave + "/" + str(page.number) + ".jpg")
    if showPrints: print("Converting PDF pages to JPG pages done")

def main(bookName):
    db = mysql.connector.connect(host="localhost", user="tfs", password="3sHUCwk3)%$%?Q5U", database="baza_wynikowa")
    cur = db.cursor()

    bookName = os.path.splitext(bookName)[0]

    cur.execute("INSERT INTO ksiazki (nazwa, sciezka) VALUES (%s, %s)", (bookName, PDFFileDirName + "/" + bookName + ".pdf"))
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    bookID = int(cur.fetchone()[0])
    db.close()

    convertPDFPagesToJPG(bookName, bookID)
    scanPages(bookName, bookID)
    
    if showPrints: print("Finished")
