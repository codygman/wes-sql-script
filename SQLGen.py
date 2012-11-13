def CreateTableSQL(tableName, columnName, columnType):
    if (len(columnName) != len(columnType)):
        return "The number of items in columnName list and columnType list is not equal."
    SQL = "CREATE TABLE IF NOT EXISTS " + tableName + "\n("
    for i in range(0, len(columnName)):
        if (i < len(columnName) - 1):
            SQL = SQL + "\n" + str(columnName[i]) + " " + str(columnType[i]) + ","
        else:
            SQL = SQL + "\n" + str(columnName[i]) + " " + str(columnType[i])
    SQL = SQL + "\n)"
    return SQL

def InsertIntoSQL(tableName, columnName, columnVal):
    if (len(columnName) != len(columnVal)):
        return "The number of items in columnName list and columnType list is not equal."
    SQL = "INSERT INTO " + str(tableName) + " \n("
    for i in range(0, len(columnName)):
        if (i < len(columnName) - 1):
            SQL = SQL + str(columnName[i]) + ","
        else:
            SQL = SQL + str(columnName[i])
    SQL = SQL + ")\nVALUES\n("
    for i in range(0, len(columnVal)):
        if (i < len(columnName) - 1):
            SQL = SQL + str(columnVal[i]) + ","
        else:
            SQL = SQL + str(columnVal[i])
    SQL = SQL + ")"
    return SQL


def getCSVRows(path):
    import csv
    iFile = open(path, "rb")
    reader = csv.reader(iFile)
    
    rowList = []
    i = 0 #COUNTER
    for row in reader:
        rowList.append(row)
        i = i + 1
    i = 0 # Reset counter
    return rowList
    

#FUNCTION DEPENDENCIES
#    getCSVRows
def InsertIntoGenCSV(tableName, path):
    rowList = getCSVRows(path)
    
    sqlTop = "INSERT INTO " + str(tableName) + "("
    for i in range(0, len(rowList[0])):
        if (i < len(rowList[0]) - 1):
            sqlTop = sqlTop + rowList[0][i] + ", "
        else:
            sqlTop = sqlTop + rowList[0][i]
    sqlTop = sqlTop + ")\nVALUES ("
    
    
    SQL = ""
    SQLLine = []
    for row in range(1, len(rowList)):
        for col in range(0, len(rowList[0])):
            if (col < len(rowList[0]) - 1):
                SQL = SQL + '"' + (rowList[row][col] + '", ')
            else:
                SQL = SQL + '"' + rowList[row][col] + '"'
        SQL = sqlTop + SQL + ")\n"
        SQLLine.append(SQL)
        SQL = ""
    
    for i in range(0, len(SQLLine)):
        SQL = SQL + SQLLine[i] + "\n"   
         
    return SQL
        