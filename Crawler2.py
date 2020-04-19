import os
import re
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve

class Crawler1:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url) # 對網站發出請求
        page = soup(html.text,'html.parser') # 解析html
        self.script = page.find_all("script")[4].text # 所需資料在第5個script標籤

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
        comment = dict()
        # 文章圖片網址、愛心數、留言數的正則表達式   
        LIKEre = re.compile(r"(https:\/\/[\w\W]*)(\",\"edge_liked_by\":{\"count\":)(\d*)")
        COMre = re.compile(r"(edge_media_to_comment\":{\"count\":)(\d*)")
        content = content.split("shortcode") # 每篇文章是以屬性shortcode作分段，其中個人照片網址只存在於第一段

        print(content)
        for article in content:
            # 取得文章圖片網址、愛心數、留言數
            getlike = LIKEre.search(article)
            getcomment = COMre.search(article)
     
            if getlike != None:
                # 將文章圖片網址、愛心數、留言數紀錄於字典

                like[getlike.group(1)] = int(getlike.group(3).replace(",",""))
                comment[ getlike.group(1)] = int(getcomment.group(2).replace(",",""))
                
        print(like)
        print(comment)
      
        return like, comment

    def Statistic(self, like, comment):
        # 原本的like、comment字典形式為[圖片網址:愛心數]、[圖片網址:留言數]
        # 為了以愛心數、留言數做鍵查詢將字典形式改為[愛心數:圖片網址]、[留言數:圖片網址]
        TransLike = {v : k for k, v in like.items()}
        TransComm = {v : k for k, v in comment.items()}
        # 取得最高愛心數、最高留言數、最低愛心數、最低留言數文章
        Most_Liked_Posts = TransLike[max(like.values())]
        Most_Commented_Posts = TransComm[max(comment.values())]
        
        return Most_Liked_Posts, Most_Commented_Posts
    
    def SaveImage(self, img, path, account):
        img_path = os.path.join("C:/Users/m4104/Desktop/InstagramBot-project/"+path+"/"+account)
        urlretrieve(img, img_path)
        
    def Run(self, account="ID"):
        like, comment = self.ProInfo(self.script)
        Most_Liked_Posts, Most_Commented_Posts = self.Statistic(like, comment)
        
        # 將個人照片、最最高愛心數、最高留言數、最低愛心數、最低留言數文章圖片儲存
        self.SaveImage(Most_Liked_Posts, "mostlike", account)
        self.SaveImage(Most_Commented_Posts, "mostcomment", account)
        
        return like[Most_Liked_Posts], comment[Most_Commented_Posts]

if __name__ == '__main__':
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    
    Crawler = Crawler1(url)
    followers, followed, article = Crawler.RE(Crawler.script)
    Most_Liked_Posts, Most_Commented_Posts  = Crawler.Run()
    #Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Crawler.Statistic(like, comment)