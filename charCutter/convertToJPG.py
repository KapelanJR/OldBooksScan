import os
import fitz
import threading

PDFdirPath = os.path.dirname(__file__) + "/../input/pdf"
JPGdirPath = os.path.dirname(__file__) + "/../input/jpg"

def generateJPGs(bookName):
    book = fitz.open(PDFdirPath + "/" + bookName)
    dirToSave = JPGdirPath + "/fromPDF_" + bookName
    if not os.path.exists(dirToSave): os.makedirs(dirToSave)
    for page in book: page.getPixmap(matrix=fitz.Matrix(8, 8)).writeImage(JPGdirPath + "/fromPDF_" + bookName + "/" + str(page.number) + ".jpg")
    print("Book: " + bookName + " done")

def main():
    booksNames = os.listdir(PDFdirPath)
    if len(booksNames) > 0:
        threads = []
        print("Converting PDFs to JPGs...")
        for bookName in booksNames:
            thread = threading.Thread(target=generateJPGs, args=[bookName])
            thread.start()
            threads.append(thread)

        for thread in threads: thread.join()
        print("Finished")

if __name__ == "__main__":
    main()