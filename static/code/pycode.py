from selenium import webdriver
from instagramUserinfo import name , password
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error

class Instagram:
    def __init__(self,name,passw):
        self.browser=webdriver.Chrome()
        self.browser.set_window_size(900,900)
        self.name=name
        self.passw=password
     
    

 
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
  
        nameInput=self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
        passwordInput=self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
        nameInput.send_keys(self.name)
        passwordInput.send_keys(self.passw)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
       






    def getFollowers(self):
  
        self.browser.get("https://www.instagram.com/"+self.name)
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        
        time.sleep(2)
        dialog=self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        followersCount = len(dialog.find_elements_by_css_selector("li"))
        
    
       
        
        while True:

            dialog.click() #ul gelir
           
            self.browser.find_element_by_xpath('/html/body').send_keys(Keys.END)
            time.sleep(2)
            newCount=len(dialog.find_elements_by_css_selector("li"))
        
            time.sleep(2)
            
            if newCount != followersCount:
                followersCount = newCount
                
                
                
            else:
                 break
          

         
        try:

            connection = mysql.connector.connect(host='127.0.0.1',
                                                    user='root',
                                                    
                                                    password='elso3306',
                                                    database='labinstagram')
            cursor=connection.cursor()
       
        except Error as e:
            print("Error while connecting to MySQL", e)   
        time.sleep(2)
        followers=dialog.find_elements_by_css_selector("li")
        #followers tablosuna kaydetmemizlazım
        
        for user in followers:

            link=str(user.find_element_by_css_selector("a").get_attribute("href"))
            link=link[26:-1]
           
            
            sql="INSERT INTO followers (name) VALUES ('{}');".format(link)
            cursor.execute(sql)
            connection.commit()
            
            

       
    

    def getFollowing(self):
        self.browser.get("https://www.instagram.com/"+self.name)
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        
        time.sleep(2)
        dialog=self.browser.find_element_by_css_selector("div[role=dialog] ul")

        followersCount=len(dialog.find_elements_by_css_selector("li"))
        
        #action=webdriver.ActionChains(self.browser)#browserı kıpırdatıyoruz
 

        while True:
            dialog.click() #ul gelir
            
            self.browser.find_element_by_tag_name('body').send_keys(Keys.END)
            
            time.sleep(2)
            newCount=len(dialog.find_elements_by_css_selector("li"))

            if newCount != followersCount:
                followersCount=newCount
               
                
                
            else:
                break
        try:
            connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram')
            cursor=connection.cursor()
        
        except Error as e:
            print("Error while connecting to MySQL", e)   
     
        followers=dialog.find_elements_by_css_selector("li")
            
            
        for user in followers:

            link=str(user.find_element_by_css_selector("a").get_attribute("href"))
            link=link[26:-1]
            print(str(link))
                
            sql="INSERT INTO following (name) VALUES ('{}');".format(link)
            cursor.execute(sql)
            connection.commit()
            


            

    def save_photo_followers(self):
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
      
       
        
        i=0
        while i<followerrs:
         
            time.sleep(1)
            sql="SELECT name FROM followers LIMIT {},{};".format(i,i+1)
            
            cursor.execute(sql)
           
          
            record = cursor.fetchone()
            user_name=record[0]
           
            
            
           
       
            self.browser.get("https://www.instagram.com/"+user_name)
 
            last_height=self.browser.execute_script("return document.documentElement.scrollHeight")
         

            while True:
                self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
                
                new_height=self.browser.execute_script("return document.documentElement.scrollHeight")
              
                if last_height == new_height:
                    break
                
                last_height = new_height



            thebox=self.browser.find_element_by_css_selector("article")
            resimler=thebox.find_elements_by_css_selector("img")
            
            sql="SELECT table_name FROM information_schema.tables WHERE table_schema = 'labinstagram';"
           
            
            cursor.execute(sql)
   
          
            recor = cursor.fetchall()
             
            deneme=0
               
            leng=len(recor)
            
            d=0
        
            while d < leng:
               
                if recor[d][0]==user_name:
                    deneme=1
                    break
                else:
                    d+=1
                
            
            
            if deneme == 1:
                pass
            else:

                sql="CREATE TABLE `{}` (name VARCHAR(30), pict VARCHAR(255))".format(user_name)
               
                cursor.execute(sql)
                
                connection.commit()
                
                for user in resimler:
                    png=user.get_attribute("src")
                    
                    sql="INSERT INTO `{}` (pict) VALUES ('{}');".format(user_name,png)
                   
                   
                    cursor.execute(sql)
                    
                    
                    connection.commit()
                    
            i=i+1



    def save_photo_following(self):

        try:

            connection=mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
            cursor=connection.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)            
        cursor.execute("SELECT COUNT(name) FROM following")
        records = cursor.fetchone()
        followingg=records[0]       
        i=0
        while i<followingg:
            time.sleep(1)
            sql="SELECT name FROM following LIMIT {},{};".format(i,i+1)
            cursor.execute(sql)       
            record = cursor.fetchone()
            user_name=record[0]
       
            self.browser.get("https://www.instagram.com/"+user_name)
            last_height=self.browser.execute_script("return document.documentElement.scrollHeight")        
            while True:
                self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")              
                new_height=self.browser.execute_script("return document.documentElement.scrollHeight")
                if last_height == new_height:
                    break
                
                last_height = new_height

            thebox=self.browser.find_element_by_css_selector("article")
            resimler=thebox.find_elements_by_css_selector("img")
            sql="SELECT table_name FROM information_schema.tables WHERE table_schema = 'labinstagram';"
            cursor.execute(sql)
            recor = cursor.fetchall()             
            deneme=0
            leng=len(recor)
            d=0       
            while d < leng:
                if recor[d][0]==user_name:
                    deneme=1
                    break
                else:
                    d+=1
            
            if deneme == 1:
                pass
            else:

                sql="CREATE TABLE `{}` (name VARCHAR(30), pict VARCHAR(255))".format(user_name)
                cursor.execute(sql)
                connection.commit()
                
                for user in resimler:
                    png=user.get_attribute("src")
                    time.sleep(1)
                    sql="INSERT INTO `{}` (pict) VALUES ('{}');".format(user_name,png)
                  
                    cursor.execute(sql)
                    connection.commit()
                    
            i=i+1
        

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
        time.sleep(1)
        cursor.execute(sql)
        record = cursor.fetchone()
        t=record[0]
        takip_ediyorsun=0
        i=i+1
        a=digerfollowing
        y=0
        while y<a:
            sql="SELECT name FROM following LIMIT {},{};".format(y,y+1)
            time.sleep(1)
            cursor.execute(sql)
            recorr = cursor.fetchone()
            denem=recorr[0]
            y+=1            
            if t == denem:
                takip_ediyorsun=1
                break
        if takip_ediyorsun == 0:
            a=open("takipettmedigin_takipci.txt","a")
            a.write(t+"\n")
            a.close()
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
        time.sleep(1)
        time.sleep(2)
        record = cursor.fetchone()
        user_name_following=record[0]
        takip_etmiyor=0
        t=t+1
        f=followerrs
        
        i=0
        while i<f:
            
            sql="SELECT name FROM followers LIMIT {},{};".format(i,i+1)
            print(sql)
            time.sleep(1)
            cursor.execute(sql)
            time.sleep(1)
            time.sleep(2)
            recorr = cursor.fetchone()
            denem=recorr[0]       
            i=i+1
            
            if user_name_following == denem:
                
                takip_etmiyor=1
                
                break
            else:
                
                takip_etmiyor=0
            
        if takip_etmiyor == 0:
            a=open("takipettigin_takipetmeyen.txt","a")
            a.write(user_name_following+"\n")
            a.close()
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
    cursor.execute("DELETE FROM following")
    connection.commit()
    cursor.execute("DELETE FROM followers")
    connection.commit()
    cursor.close()


instagram=Instagram(name,password)
instagram.signIn()
time.sleep(2)

instagram.getFollowers()

instagram.getFollowing()
instagram.save_photo_followers()
instagram.save_photo_following()
takip_etmeyen()
takipetmedigintakipci()
db_delete()




