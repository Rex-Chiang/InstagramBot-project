import time
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver

class Crawler:
    def __init__(self, url):
        self.url = url
        
        file = open('C:/Users/m4104/Desktop/InstagramBot-project/userfile.txt','r')
        userfile = file.readlines()
        self.user = userfile[0].rstrip()
        self.pwd = userfile[1].rstrip()
 
        chrome_options = webdriver.ChromeOptions() # 對Chrome瀏覽器設定
        #chrome_options.add_argument('--headless') # 啟動無頭模式，不顯示瀏覽畫面
        chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"') # 設定user agent
        self.driver = webdriver.Chrome(executable_path='C:/Users/m4104/Desktop/InstagramBot-project/chromedriver', chrome_options=chrome_options)
        self.driver.get(self.url) # 對網站發出請求
        
        self.login()
        self.follow()
        #page = soup(driver.page_source,'html.parser')
        self.close()
        
    def login(self):
        time.sleep(3)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='username']").send_keys(self.user)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='password']").send_keys(self.pwd)
        self.driver.find_element_by_xpath("//div/button[@type='submit']").click()
        
    def follow(self):
        time.sleep(3)
        self.driver.get("https://www.instagram.com/explore/people/suggested/")
        time.sleep(3)
        follow_list = self.driver.find_elements_by_xpath("//div/div/button[contains(text(), '追蹤')]")
        for i in range(0, 3):
            follow_list[i].click()
            time.sleep(1)
    
    def close(self):
        self.driver.close()


if __name__ == '__main__':
    
    url = "https://www.instagram.com"
    
    Crawler = Crawler(url)