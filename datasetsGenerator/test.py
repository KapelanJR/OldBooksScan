import os
import fitz

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


bookPath = os.path.dirname(__file__) + "/books/book1.pdf"
doc = fitz.open(bookPath)
page = doc[12]
text = page.getText("rawdict", flags=fitz.TEXT_PRESERVE_LIGATURES + fitz.TEXT_PRESERVE_WHITESPACE)
textBlocks = text["blocks"]
char = 'a'
areas = searchForCaseSensitive(textBlocks, char)
print("TEST")
