import time

import mysql.connector
from mysql.connector import Error



def db_delete():
    try:

        connection=mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)   
    time.sleep(2)
         #following tablosu silinecek follow tablosu silinecek 
    
    cursor.execute("DELETE FROM followers")
    connection.commit()
    
    cursor.close()


db_delete()