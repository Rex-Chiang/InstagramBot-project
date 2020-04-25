import time
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class Crawler:
    def __init__(self, url):
        self.url = url
        self.follow_name = []
        
        file = open('C:/Users/m4104/Desktop/InstagramBot-project/userfile.txt','r')
        userfile = file.readlines()
        self.user = userfile[0].rstrip()
        self.pwd = userfile[1].rstrip()
 
        chrome_options = webdriver.ChromeOptions() # Set Chrome browser
        #chrome_options.add_argument('--headless') # Start the headless mode
        chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"')
        chrome_options.add_experimental_option("mobileEmulation", {'deviceName': 'iPhone 8'})
        self.driver = webdriver.Chrome(executable_path='C:/Users/m4104/Desktop/InstagramBot-project/chromedriver', chrome_options=chrome_options)
        self.driver.get(self.url)
        
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
        for i in range(0, 5):
            follow_list[i].click()
            time.sleep(1)
            
    # Only get the recently part of follow.
    def get_follow(self):
        time.sleep(3)
        self.driver.get("https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%2233251935508%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D")
        time.sleep(3)
        page = soup(self.driver.page_source,'html.parser')
        text = page.find("pre").text
        user_data = json.loads(text)["data"]["user"]["edge_follow"]["edges"]
        
        for user in user_data:
            self.follow_name.append(user["node"]["username"])
    
    def un_follow(self):
        self.driver.find_element_by_xpath("//button/div/span[@aria-label='追蹤中']").click()
        self.driver.find_element_by_xpath("//div/button[contains(text(), '取消追蹤')]").click()
        
    def check_follow(self):
        for name in self.follow_name:
            url = "https://www.instagram.com/" + name
            self.driver.get(url)
            time.sleep(3)
            page = soup(self.driver.page_source,'html.parser')
            user_info = page.find_all("span",attrs={"class":"g47SY"})
            follow_count = user_info[1]["title"]
            print(name, ":", follow_count)

            if int(follow_count.replace(",", "")) < 1000:
                self.un_follow()
                self.follow_name.remove(name)
                
    def post(self):
        time.sleep(3)
        element = self.driver.find_element_by_tag_name('body')
        element.send_keys(Keys.F12)
       # builder = ActionChains(self.driver)
       # builder.key_down(Keys.F12).perform()
        time.sleep(3)

    def close(self):
        self.driver.close()
        
    def log(self):
        time.sleep(3)
        self.driver.find_element_by_xpath("//div/button[contains(text(), '登入')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='username']").send_keys(self.user)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='password']").send_keys(self.pwd)
        self.driver.find_element_by_xpath("//div/button/div[contains(text(), '登入')]").click()
        


if __name__ == '__main__':
    
    url = "https://www.instagram.com"
    
    Crawler = Crawler(url)
    Crawler.log()
    #Crawler.post()