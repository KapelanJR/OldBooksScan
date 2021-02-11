import mysql.connector
import json

def getTableNames(cur):
    cur.execute("SHOW TABLES")
    return [name[0] for name in cur.fetchall()]

def getColumnNames(cur, tableName):
    cur.execute("SHOW columns FROM " + tableName)
    return [name[0] for name in cur.fetchall()]

def generateListOfDictFromTable(cur, tableName):
    columnNames = getColumnNames(cur, tableName)
    listOfRowDict = []
    cur.execute("SELECT * FROM " + tableName)
    rows = cur.fetchall()
    for row in rows:
        listOfRowDict.append({})
        for i in range(len(columnNames)):
            listOfRowDict[-1][columnNames[i]] = row[i]

    return listOfRowDict

def main():
    db = mysql.connector.connect(
        host = "localhost",
        user = "tfs",
        password = "3sHUCwk3)%$%?Q5U",
        database = "baza_wynikowa"
    )

    cur = db.cursor()
    tableNames = getTableNames(cur)
    dictForJSON = {}
    for tableName in tableNames: dictForJSON[tableName] = generateListOfDictFromTable(cur, tableName)
    
    with open("database.json", "w", encoding = "utf-8") as jsonFile:
        json.dump(dictForJSON, jsonFile, ensure_ascii = False, indent = 4)

if __name__ == "__main__":
    main()