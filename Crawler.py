import time
import requests
import json
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
        self.check_follow()
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
            
    def check_follow(self):
        time.sleep(3)
        self.driver.get("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%2233251935508%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D")
        time.sleep(3)
        page = soup(self.driver.page_source,'html.parser')
        text = page.find("pre").text
        user_data = json.loads(text)["data"]["user"]["edge_follow"]["edges"]
        
        follow_name = []
        for user in user_data:
            follow_name.append(user["node"]["username"])
    
    def close(self):
        self.driver.close()


if __name__ == '__main__':
    
    url = "https://www.instagram.com"
    
    Crawler = Crawler(url)