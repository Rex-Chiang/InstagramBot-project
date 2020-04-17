import time
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver

class Crawler:
    def __init__(self, url):
        self.url = url
        
        file = open('C:/Users/m4104/Desktop/InstagramBot-project/userfile.txt','r')
        userfile = file.readlines()
        user = userfile[0].rstrip()
        pwd = userfile[1].rstrip()
 
        chrome_options = webdriver.ChromeOptions() # 對Chrome瀏覽器設定
        chrome_options.add_argument('--headless') # 啟動無頭模式，不顯示瀏覽畫面
        chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"') # 設定user agent
        driver = webdriver.Chrome(executable_path='C:/Users/m4104/Desktop/InstagramBot-project/chromedriver', chrome_options=chrome_options)
        driver.get(self.url) # 對網站發出請求
        time.sleep(3)
        driver.find_element_by_xpath("//div/div/label/input[@name='username']").send_keys(user)
        driver.find_element_by_xpath("//div/div/label/input[@name='password']").send_keys(pwd)
        driver.find_element_by_xpath("//div/button[@type='submit']").click()
        time.sleep(3)
        #driver.get("https://www.instagram.com/apple.punching/following/")
        #page = soup(driver.page_source,'html.parser')
        #print(page)
        driver.close()


if __name__ == '__main__':
    
    url = "https://www.instagram.com"
    
    Crawler = Crawler(url)