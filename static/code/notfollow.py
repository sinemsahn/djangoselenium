from selenium import webdriver
from instagramUserinfo import name , password
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error

def takipetmedigintakipci():
    try:
        connection=mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
    except Error as e:
        print("Error while connecting to MySQL", e)   
    cursor.execute("SELECT COUNT(name) FROM followers")
    records = cursor.fetchone()
    followerrs=records[0]
    cursor.execute("SELECT COUNT(name) FROM following")
    records = cursor.fetchone()
    digerfollowing=records[0]
    i=0

    while i<followerrs:
        sql="SELECT name FROM followers LIMIT {},{};".format(i,i+1)
       # time.sleep(1)
        cursor.execute(sql)
        record = cursor.fetchone()
        t=record[0]
        takip_ediyorsun=0
        i=i+1
        a=digerfollowing
        y=0
        #print(t+"aranacak olan")
        while y<a:
            sql="SELECT name FROM following LIMIT {},{};".format(y,y+1)
            #print(sql)
            time.sleep(1)
            cursor.execute(sql)
            recorr = cursor.fetchone()
            denem=recorr[0]
            y+=1   
           # print(denem+ "bakıyor")         
            if t == denem:
                #print(t+"buldu")

                takip_ediyorsun=1
                break
        if takip_ediyorsun == 0:
            sql="INSERT INTO notfollow (name) VALUES ('{}');".format(t)
            cursor.execute(sql)
            connection.commit()


takipetmedigintakipci()
