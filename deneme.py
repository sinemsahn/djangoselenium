import mysql.connector
from mysql.connector import Error



try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
    cursor=connection.cursor()
        
except Error as e:
    print("Error while connecting to MySQL", e)
sql="SELECT pict FROM muthispsikoloji ;"
print(sql)
cursor.execute(sql)
m = cursor.fetchall()
connection.commit()
print(m)
print("\n")
