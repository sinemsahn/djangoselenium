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
                                                    database='labinstagram',
                                                    buffered=True)
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
    if instagram.browser != None:
        instagram.browser.quit()
time.sleep(2)
try:
    instagram.getFollowers()
except:
    if instagram.browser != None:
        instagram.browser.quit()


try:
    instagram.kapatma()
except:
    instagram.browser.quit()
