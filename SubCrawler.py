import os
import re
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve

class Crawler:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url) # 對網站發出請求
        page = soup(html.text,'html.parser') # 解析html
        self.script = page.find_all("script")[4].text # 所需資料在第5個script標籤
        if self.script == "window.__initialDataLoaded(window._sharedData);":
            self.script = page.find_all("script")[3].text# 所需資料在第4個script標籤
            
    def RE(self, content):
        # 定義被追蹤數、追蹤數、發文數的正則表達式
        FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
        FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
        ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
        # 取得追蹤數、追蹤數、發文數
        followers = FOLLOWre.search(content).group(2)
        followed = FOLLOWEDre.search(content).group(2)
        article = ARTICLEre.search(content).group(2)
        
        return followers, followed, article

    def ProInfo(self, content):
        like = dict()
        # 文章圖片網址、愛心數的正則表達式   
        LIKEre = re.compile(r"(\"display_url\"\:\")(https:\/\/[\w\W]*)(\",\"gating_info[\w\W]*)(,\"edge_liked_by\":{\"count\":)(\d*)")
        content = content.split("shortcode") # 每篇文章是以屬性shortcode作分段，其中個人照片網址只存在於第一段
        
        for article in content:
            # 取得文章圖片網址、愛心數
            getlike = LIKEre.search(article)
            
            if getlike != None:
                # 將文章圖片網址、愛心數紀錄於字典
                pic_url = getlike.group(2).replace("\\u0026", "&")
                like_ct = getlike.group(5)
                like[pic_url] = like_ct
        
        return like

    def Statistic(self, like):
        try:
            # 原本的like字典形式為[圖片網址:愛心數]
            # 為了以愛心數做鍵查詢將字典形式改為[愛心數:圖片網址]
            TransLike = {v : k for k, v in like.items()}
            # 取得最高愛心數
            Most_Liked_Posts = TransLike[max(like.values())]
        except:
            raise
            return
        
        return Most_Liked_Posts
    
    def SaveImage(self, img, account):
        img_path = os.path.join("C:/Users/m4104/Desktop/InstagramBot-project/mostlike/"+account)        
        urlretrieve(img, img_path + ".png")
        
    def Run(self, account="ID"):
        like = self.ProInfo(self.script)
        Most_Liked_Posts = self.Statistic(like)
        
        # 將個人照片、最最高愛心數文章圖片儲存
        self.SaveImage(Most_Liked_Posts, account)
        
        return like[Most_Liked_Posts]

if __name__ == '__main__':
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    
    Crawler = Crawler(url)
    followers, followed, article = Crawler.RE(Crawler.script)
    Most_Liked_Posts  = Crawler.Run(ID)