

'''
import mysql.connector
from mysql.connector import Error


try:
    connection=mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
    cursor=connection.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)   
cursor.execute("SELECT name FROM users")
records = cursor.fetchall()
followerrs=records[-1]
followerrs=followerrs[0]
name=followerrs

cursor.execute("SELECT password FROM users")
records = cursor.fetchall()
followerrs=records[-1]
followerrs=followerrs[0]
password=followerrs

'''



name="sinems_hn"
password="fenerFB1.wert"



