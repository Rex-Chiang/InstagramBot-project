import time
import json
import os
import sys
import traceback
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC

class Crawler:
    def __init__(self, url, mobile = False):
        self.url = url
        self.follow_name = []
        
        file = open('C:/Users/m4104/Desktop/InstagramBot-project/userfile.txt','r')
        userfile = file.readlines()
        self.user = userfile[0].rstrip()
        self.pwd = userfile[1].rstrip()
 
        chrome_options = webdriver.ChromeOptions() # Set Chrome browser
        chrome_options.add_argument('--headless') # Start the headless mode

        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        if mobile:
            user_agent = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
            mobileEmulation = {"deviceMetrics": {"width": 400, "height": 550, "pixelRatio": 3.0}, "userAgent": user_agent}
            chrome_options.add_experimental_option("mobileEmulation", mobileEmulation)
        else:
            chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"')
        
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
        for i in range(0, 10):
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

    def close(self):
        self.driver.close()
        
    def exception(self, e):
        detail = e.args[0] # get detail of exception
        cl, exc, tb = sys.exc_info() # get Call Stack

        lastCallStack = traceback.extract_tb(tb)[0] # get Call Stack first data
        fileName = lastCallStack[0] # get exception file name 
        lineNum = lastCallStack[1] # get exception line
        funcName = lastCallStack[2] # get exception function
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, detail)
        print(errMsg)
        
    def log_mobile(self):
        print("----------------- Mobile Login -----------------")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/button[contains(text(), '登入')]")))
        element.click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='username']").send_keys(self.user)
        self.driver.find_element_by_xpath("//div/div/label/input[@name='password']").send_keys(self.pwd)
        self.driver.find_element_by_xpath("//div/button/div[contains(text(), '登入')]").click()
        
        print("----------------- Mobile Login Complete-----------------")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/button[contains(text(), '稍後再說')]")))
        element.click()
        #element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/button[contains(text(), '取消')]")))
        #element.click()
    
    def post(self, name, path):
        pic = path + name +".png"
        tag = "//button/div/img[@alt='" + name + " 的大頭貼照']"

        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div[@data-testid='new-post-button']")))
        element.click()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/form/input[@accept='image/jpeg']")))
        element.send_keys(pic)        
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/button[contains(text(), '繼續')]")))
        element.click()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//section/div/textarea[@aria-label='輸入說明文字……']")))
        element.send_keys("@" + name + "\n#instagood#love#beautiful#cute#like4like#followme")         
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body/div[@id='react-root']")))
        element.click()
        
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/section/button/span[contains(text(), '標註人名')]")))
            element.click()
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/img[@alt='可標註的相片']")))
            element.click()
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/label/input[@placeholder='搜尋']")))
            element.send_keys(name) 
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, tag)))
            element.click()
        
        except Exception as e:
            print(name, ":Fail to tag the picture")
            self.exception(e)
        
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/button[contains(text(), '完成')]")))
        element.click()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div/div/button[contains(text(), '分享')]")))
        element.click()
        
if __name__ == '__main__':
    
    url = "https://www.instagram.com"
    
    Crawler = Crawler(url)
    Crawler.log_mobile()
    
    path = "C:/Users/m4104/Desktop/InstagramBot-project/mostlike/"
    names = os.listdir(path)
    for name in names:
        Crawler.post(name.split(".png")[0], path)
        os.remove(path + name)
    #Crawler.post("xiangjessie")