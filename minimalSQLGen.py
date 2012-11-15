# http://www.census.gov/tiger/tms/gazetteer/zips.txt

import csv

# assuming schema of:
#mysql> describe geodata;
# +----------+-------------+------+-----+---------+----------------+
# | Field    | Type        | Null | Key | Default | Extra          |
# +----------+-------------+------+-----+---------+----------------+
# | id       | int(11)     | NO   | PRI | NULL    | auto_increment |
# | zip_code | int(5)      | NO   |     | NULL    |                |
# | state    | varchar(2)  | NO   |     | NULL    |                |
# | city     | varchar(6)  | NO   |     | NULL    |                |
# | lat      | float(10,6) | NO   |     | NULL    |                |
# | long     | float(10,6) | NO   |     | NULL    |                |
# +----------+-------------+------+-----+---------+----------------+
# 6 rows in set (0.00 sec)

ALLSQL = []
# creates this list:
# ['INSERT', 'INTO', 'geodata(zip_code,', 'state,', 'city,', 'lat,', 'long)', 'VALUES(']

#I am going to read all values into a tuple (unmodifiable list)
# then I'll extend the SQL list, and append it to ALLSQL
with open('zips.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        #SQL = "INSERT INTO geodata(zip_code, state, city, lat, long) VALUES(".split()
        SQL = ['INSERT', 'INTO', 'geodata(zip_code,', 'state,', 'city,', 'lat,', 'long)', 'VALUES(']     
        #if i > 20:
        #    break
        values = [row[0], row[1], row[2], row[3], row[4]]
        SQL.extend(values)
        SQL.append(");")
        ALLSQL.append(SQL)

with open('zips.sql', 'wb') as f:
    f.write(' '.join([' '.join(sql) for sql in ALLSQL]))
