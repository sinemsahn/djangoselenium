from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.contrib import messages


from selenium import webdriver

import time
from selenium.webdriver.common.keys import Keys
import mysql.connector
from mysql.connector import Error
from webdriver_manager.chrome import ChromeDriverManager

# Create your views here.
def form(request):
    # form düzenle req olarak
    #formu göstercek
    return render(request,'form.html',{})
def index(request):
    #ana sayfam
    return render(request,'index.html',{})
def hata(request):
    return render(request,'404.html',{})

def sonuc(request):
    #gelen veri db ye kaydetmeden önce burdaalınıp kontrol edilcek
    #hata gelirse hata 404 sayfaına 
    # değilse db ye kaydet diğer işlem fonksiyonuna
    #orda hata gelirse 404 yoksa selenium devam iş bitince sonuca
    if request.method == 'POST':
        username=request.POST.get('username')
        parola=request.POST.get('password')
        try:
            try:


                connection = mysql.connector.connect(host='127.0.0.1',
                                                                user='root',
                                                                
                                                                password='elso3306',
                                                                database='labinstagram',
                                                                buffered=True)
                cursor=connection.cursor()    
            except Error :
                return render(request,'404.html',{}) # bunlarıredirect yap
            sql="INSERT INTO  users (name,password) VALUES ('{}','{}');".format(username,parola)
            cursor.execute(sql)
            connection.commit()   
        except Error :
            return render(request,'404.html',{}) # bunlarıredirect yap
        return render(request,'sonuc.html',{'username':username,'parola':parola})
    else :
        return render(request,'404.html',{})  
    #return render(request,'sonuc.html',{'username':username,'password':password})

    #kayıttamam ve doğruysa seleniuma yolla değilse  404 verdir button ile forma gitsin 
    #password düzeltilmeli
    

##şimdilik kayıt atana kadar ki kısım 
# sonra selenium fonksiyonuunu çalıştır
# sonra celery

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            userr = authenticate(username=username, password=raw_password)
            login(request, userr)
        
            try:
                try:


                    connection = mysql.connector.connect(host='127.0.0.1',
                                                                    user='root',
                                                                    
                                                                    password='elso3306',
                                                                    database='labinstagram',
                                                                    buffered=True)
                    cursor=connection.cursor()    
                except Error :
                    return render(request,'404.html',{}) # bunlarıredirect yap
                sql="INSERT INTO  users (name,password) VALUES ('{}','{}');".format(username,raw_password)
                cursor.execute(sql)
                connection.commit()   
            except Error :
                return render(request,'404.html',{}) # bunlarıredirect yap

            return render(request,'sonuc.html',{'userr':userr})
        
            
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def gorbutton(request,username,id):
    # gelen kullanıcı parola ile şimdilik selenium ile giriş yapıp çıksın
    #ilk olarak dbden bu kullanıcıya ait bilgileri mysqlden çekelim
    # sonra selenium kodlarım çalışsın
    class Instagram:
        def __init__(self,name,passw):
            self.browser=webdriver.Chrome(ChromeDriverManager().install())
            self.browser.set_window_size(900,900)
            self.name=name
            self.passw=passw
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
        def getFollowing(self):

            self.browser.get("https://www.instagram.com/"+self.name)
            time.sleep(2)
            self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
            
            time.sleep(1)
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
                                                            database='labinstagram',
                                                            buffered=True)
                cursor=connection.cursor()
            
            except Error as e:
                print("Error while connecting to MySQL", e)   
        
            followers=dialog.find_elements_by_css_selector("li")
                
                
            for user in followers:

                link=str(user.find_element_by_css_selector("a").get_attribute("href"))
                link=link[26:-1]
                
                    
                sql="INSERT INTO following (name) VALUES ('{}');".format(link)
                cursor.execute(sql)
                connection.commit()
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
        cursor.execute("DELETE FROM notfollow")
        connection.commit()
        cursor.execute("DELETE FROM notfollowing")
        connection.commit()
        cursor.close()

 
   
   
   
   
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT password FROM users WHERE name = '{}';".format(username)
    cursor.execute(sql)
    m=cursor.fetchone()
    connection.commit()
    password= m[0]
    #çağırmaişlemleri ve fonksiyonu çalıştırma

    instagram=Instagram(username,password)
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
        instagram.getFollowing()
    except:
        if instagram.browser != None:
            instagram.browser.quit()
    try:
        instagram.save_photo_following()
    except:
        if instagram.browser != None:
            instagram.browser.quit()

    

    try:
        instagram.kapatma()
    except:
        instagram.browser.quit()
    
    # seleniumile işlmeler tamam db ye yazmış olacak diğer notları da db ye yazacak gösterilecek olanları alalım sonrası sil 
    takipetmedigintakipci()
    takip_etmeyen()
    
    
    
    
    
    
    
    #en son almaişlemleri followers following notfollow not following
    
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT * FROM followers "
    cursor.execute(sql)
    followw=cursor.fetchall()
    connection.commit()


    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT * FROM following "
    cursor.execute(sql)
    followingg=cursor.fetchall()
    connection.commit()


    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT * FROM notfollow"
    cursor.execute(sql)
    notfolloww=cursor.fetchall()
    connection.commit()

    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT * FROM notfollowing "
    cursor.execute(sql)
    notfollowingg=cursor.fetchall()
    connection.commit()


    #sil dbleri ve postu 
    try:
        post=get_object_or_404(User,id=id)
    #silincek postu getiriyoruz
        post.delete()
        messages.success(request, "The user is deleted")            

    except Error: 
        return render(request, '404.html')
    
    db_delete()

    
    return render(request,'finish.html',{'followw':followw,'followingg':followingg,'notfolloww':notfolloww,'notfollowingg':notfollowingg})

        

def deleteuserbutton(request,id):
    try:
        post=get_object_or_404(User,id=id)
    #silincek postu getiriyoruz
        post.delete()
        messages.success(request, "The user is deleted")            

    except Error: 
        return render(request, '404.html')
    #return render(request, 'signup.html',{'form':form}) 
    return redirect("/signup")

'''    
def deneme(request,username):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
        cursor=connection.cursor()
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    sql="SELECT password FROM users WHERE username = '{}';".format(username)
    cursor.execute(sql)
    m=cursor.fetchone()
    connection.commit()
    password= m[0]
    dosya_name= username + ".txt"
    dosya= open(dosya_name,"w")
    yaz = "username: "+ username + "\n password: "+password
    dosya.write(yaz)
'''


'''
name="sinems_hn"
password="fenerFB1.wert"
'''

