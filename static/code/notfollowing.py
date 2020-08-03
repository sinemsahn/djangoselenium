from selenium import webdriver
from instagramUserinfo import name , password
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error

def takip_etmeyen():
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
    cursor.execute("SELECT COUNT(name) FROM followers")
    records = cursor.fetchone()
    followerrs=records[0]
    cursor.execute("SELECT COUNT(name) FROM following")
    records = cursor.fetchone()
    digerfollowing=records[0]
    t=0
    while t<digerfollowing:
        sql="SELECT name FROM following LIMIT {},{};".format(t,t+1)
        time.sleep(1)
        cursor.execute(sql)
        #time.sleep(1)
        #time.sleep(2)
        record = cursor.fetchone()
        user_name_following=record[0]
        takip_etmiyor=0
        t=t+1
        f=followerrs
        
        i=0
        while i<f:
            
            sql="SELECT name FROM followers LIMIT {},{};".format(i,i+1)
            print(sql)
         #   time.sleep(1)
            cursor.execute(sql)
          #  time.sleep(1)
           # time.sleep(2)
            recorr = cursor.fetchone()
            denem=recorr[0]       
            i=i+1
            
            if user_name_following == denem:
                
                takip_etmiyor=1
                
                break
            else:
                
                takip_etmiyor=0
            
        if takip_etmiyor == 0:
            sql="INSERT INTO notfollowing (name) VALUES ('{}');".format(user_name_following)
            cursor.execute(sql)
            connection.commit()


takip_etmeyen()