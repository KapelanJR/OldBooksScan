from PIL import Image
import numpy as np
from scipy import ndimage
import os

#Ustawienia
inputDirName = "input"
outputDirName = "output"
contrastDivThreshold = 0.65 #Dzielnik kontrastu
edgesDetectionThreshold = 0.3 #Ile procent lini ma być czarne aby wykryło, że linia ta jest na końcach zdjęcia (a nie jest tekstem) i ma zostać ustawić na kolor biały 
dirtDetectionThreshold = 0.99 #Ile procent lini ma być białe, aby wykryło, że ewentualne czarne częsci nie są tekstem, a jedynie jakimś brudem


#Zmienne globalne
imgWidth = 0
imgHeight = 0

#Definicja ścieżki bezwzględnej
dirPath = os.path.dirname(__file__) + "/"

def devideContrast(pixels):
    return np.where(pixels > int(contrastDivThreshold * 255), 255, 0)

def removeEdges(pixels):
    for i in range(imgHeight):
        if np.average(pixels[i]) < (1 - edgesDetectionThreshold) * 255 or np.average(pixels[i]) > dirtDetectionThreshold * 255:
            pixels[i].fill(255)
    for i in range(imgWidth):
        if np.average(pixels[:, i]) < (1 - edgesDetectionThreshold) * 255 or np.average(pixels[:, i]) > dirtDetectionThreshold * 255:
            pixels[:, i].fill(255)
    
    return pixels

def countWhitePixelsRows(pixels):
    return imgHeight - np.count_nonzero(imgWidth - np.count_nonzero(pixels, axis=1))

def detectCorrectRotation(pixels):
    print(countWhitePixelsRows(pixels))
    pixels = ndimage.rotate(pixels, -10, reshape=False, mode="constant", cval=255, prefilter=False)
    pixels = devideContrast(pixels)
    print(countWhitePixelsRows(pixels))
    
    return pixels

def cleanPixels(pixels):
    pixels = devideContrast(pixels)
    pixels = removeEdges(pixels)
    pixels = detectCorrectRotation(pixels)
    
    return pixels


def main():
    global imgWidth
    global imgHeight

    img = Image.open(dirPath + inputDirName + "/1.jpg").convert('L')
    imgWidth, imgHeight = img.size
    pixels = np.array(img)

    pixels = cleanPixels(pixels)


    outputImg = Image.fromarray(pixels)
    outputImg.show()

if __name__ == "__main__":
    main()