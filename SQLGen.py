def CreateTableSQL(tableName, columnName, columnType):
    # less parenthesis make things more readable
    if len(columnName) != len(columnType):
        return "The number of items in columnName list and columnType list is not equal."

    # Use string formatting. The parenthesis around tableName make it a
    # tuple which is an immutable type. This is mostly there because I
    # am paranoid and I think it makes a certain type of exploit harder to
    # do, but this is from a conversation long ago :D
    SQL = "CREATE TABLE IF NOT EXISTS %s\n(" % (tableName)

    # use xrange whenever possible, it's a lazy evaluator and processes
    # one number at a time whereas range makes an entire list for you
    # to evaluate over. In python 3 however, range is the same as xrange.
    # basically lets say you have a wordlist of the entire english language,
    # if you try to do a range on that it'll create a list so big your
    # computer will run out of memory and start swapping.
    for i in xrange(0, len(columnName)):
        if (i < len(columnName) - 1):
            # string concatenation is expensive in every language, actually
            # after these initial fixes I'm going to recode this "The Python
            # Way".
            # For lower than python 2.6
            #SQL = "%s\n%s %s," % (SQL, str(columnName[i], str(columnType[i])))
            # with the .format method it's not necessary to cast types
            SQL = "{0}\n{1} {2},".format(SQL, columnName[i], columnType[i])
        else:
            SQL = "{0}\n{1} {2}".format(SQL, columnName[i], columnType[i])
    SQL = "{0}\n".format(SQL)
    return SQL

def InsertIntoSQL(tableName, columnName, columnVal):
    if len(columnName) != len(columnVal):
        return "The number of items in columnName list and columnType list is not equal."
    SQL = "INSERT INTO {0} \n(".format(tableName)
    for i in range(0, len(columnName)):
        if i < len(columnName) - 1:
            SQL = "{0}{1},".format(SQL, columnName[i])
        else:
            SQL = "{0}{1}".format(columnName[i])
    SQL = "{0})\nVALUES\n(".format(SQL)
    for i in range(0, len(columnVal)):
        if i < len(columnName) - 1:
            SQL = "{0}{1},".format(SQL, columnVal[i])
        else:
            SQL = "{0}{1}".format(SQL, columnVal[i])
    SQL = "{0})".format(SQL)
    return SQL


def getCSVRows(path):
    import csv
    iFile = open(path, "rb")
    reader = csv.reader(iFile)
    
    rowList = []
    # use enumerate and multiple variable declaration instead of a counter
    # http://docs.python.org/2/library/functions.html#enumerate
    # makes things much cleaner :D
    for i, row in enumerate(reader):
        rowList.append(row)
    return rowList
    

#FUNCTION DEPENDENCIES
#    getCSVRows
def InsertIntoGenCSV(tableName, path):
    rowList = getCSVRows(path)
    
    sqlTop = "INSERT INTO {0} (".format(tableName)
    for i in range(0, len(rowList[0])):
        if i < len(rowList[0]) - 1:
            sqlTop = "{0}{1}, ".format(sqlTop, rowList[0][i])
        else:
            sqlToP = "{0}{1}".format(sqlTop, rowList[0][i])
            # Bet you're wondering why I'm making this change. Again it has to
            # do with concatenation being so inefficient. I'm about to time it,
            # but I'm betting format is FAR faster than concat. Results below:
            # cody@zentop:~$ python -m timeit -s "s = 'stuff' + 'more stuff'"
            # 100000000 loops, best of 3: 0.0168 usec per loop
            #
            # cody@zentop:~$ python -m timeit -s "s = '{0}{1}'.format('stuff', 'more stuff')"
            # 100000000 loops, best of 3: 0.0165 usec per loop
            # 
            # Only slightly faster... let's see if it changes with a bigger string
            #
            # try 10 string concats
            # python -m timeit -s "s = 'stuff' + 'more stuff' + 'stfsduff' + 'moresafd stuff' + 'stuasaaaff' + 'more stffffuff' + 'stuaaaaaff' + 'moddddre stuff' + 'stussssff' + 'more sfdasdfstuff'"
            # 100000000 loops, best of 3: 0.017 usec per loop
            #
            # python -m timeit -s "s = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'.format('stuff', 'more stuff', 'stfsduff', 'moresafd stuff', 'stuasaaaff', 'more stffffuff', 'stuaaaaaff', 'moddddre stuff', 'stussssff', 'more sfdasdfstuff')"
            # 100000000 loops, best of 3: 0.0165 usec per loop
            # 
            # The difference is hardly noticable, but as you can see as you add more strings it gets slower at
            # a faster rate.
            # the recommended way of concatenating strings, which I suspect format is doing:
            # python -m timeit -s "''.join(['stuff', 'more stuff', 'stfsduff', 'moresafd stuff', 'stuasaaaff', 'more stffffuff', 'stuaaaaaff', 'moddddre stuff', 'stussssff', 'more sfdasdfstuff'])"
            # 100000000 loops, best of 3: 0.0165 usec per loop


            sqlTop = "{0}{1}".format(sqlTop, rowList[0][i])
    sqlTop = "{0})\nVALUES (".format(sqlTop)
    
    
    SQL = ""
    SQLLine = []
    for row in range(1, len(rowList)):
        for col in range(0, len(rowList[0])):
            if col < len(rowList[0]) - 1:
                SQL = '{0}"{1}", '.format(SQL, rowList[row][col])
            else:
                SQL = '{0}"{1}"'.format(SQL, rowList[row][col])
        SQL = "{0})\n".format(SQL)
        SQLLine.append(SQL)
        SQL = ""
    
    for i in range(0, len(SQLLine)):
        SQL = "{0}{1}\n".format(SQL, SQLLine[i])
         
    return SQL
        
