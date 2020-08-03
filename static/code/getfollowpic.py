from selenium import webdriver
from instagramUserinfo import name , password
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error
from webdriver_manager.chrome import ChromeDriverManager


class Instagram:
    def __init__(self,name,passw):
        self.browser=webdriver.Chrome(ChromeDriverManager().install())
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
    def kapatma(self):

        self.browser.get("https://www.instagram.com/"+self.name)
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div/button").click()

        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div/button[9]").click()
        time.sleep(2)
        self.browser.quit()

instagram=Instagram(name,password)
try:

    instagram.signIn()
except:
    instagram.browser.quit()


  

try:
    instagram.save_photo_followers()
except:
    instagram.browser.quit()

try:
    instagram.kapatma()
except:
    instagram.browser.quit()
