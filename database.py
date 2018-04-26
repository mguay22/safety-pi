
import mysql.connector

cnx = mysql.connector.connect(user='root', password='root', host='localhost', port='8889', database='safetypi')
print(cnx)

cnx.close()