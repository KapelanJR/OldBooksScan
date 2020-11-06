import os

dirPath = os.path.dirname(__file__)
datasetsDir = "datasets"
cleanedDir = "polish_1_fix"
toCleanDir = "polish_1_hd"

cleaned = os.listdir(dirPath + "/" + datasetsDir + "/" + cleanedDir)
toClean = os.listdir(dirPath + "/" + datasetsDir + "/" + toCleanDir)

for imgName in toClean:
    if imgName not in cleaned: 
        os.remove(dirPath + "/" + datasetsDir + "/" + toCleanDir + "/" + imgName)
        print("Removed: " + imgName)

print("Finished")
