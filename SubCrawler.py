import os
import re
import requests
import MainCrawler
import MySQLdb
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve

class Crawler:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url)
        page = soup(html.text,'html.parser')
        # Check the location of information that we need in fourth or fifth "script" tag.
        self.script = page.find_all("script")[4].text
        if self.script == "window.__initialDataLoaded(window._sharedData);":
            self.script = page.find_all("script")[3].text
        
        file = open('C:/Users/m4104/Desktop/InstagramBot-project/userfile.txt','r')
        userfile = file.readlines()
        pwd = userfile[2].rstrip()
        
        self.conn = MySQLdb.connect(port=3306, user='rex', passwd=pwd, db="instagram")
        self.cur = self.conn.cursor()
            
    def RE(self, content):
        # Define regular expression of follow, follower, post count.
        FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
        FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
        ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
        # Get follow, follower, post count.
        followers = FOLLOWre.search(content).group(2)
        followed = FOLLOWEDre.search(content).group(2)
        article = ARTICLEre.search(content).group(2)
        
        return followers, followed, article

    def ProInfo(self, content):
        like = dict()
        # Define regular expression of picture url and likes count.
        LIKEre = re.compile(r"(\"display_url\"\:\")(https:\/\/[\w\W]*)(\",\"gating_info[\w\W]*)(,\"edge_liked_by\":{\"count\":)(\d*)")
        # Each post is seperate by "shortcode" attribute
        content = content.split("shortcode")
        
        for article in content:
            # Get picture url and likes count.
            getlike = LIKEre.search(article)
            
            if getlike != None:
                # Save picture url and likes count in dict.
                pic_url = getlike.group(2).replace("\\u0026", "&")
                like_ct = getlike.group(5)
                like[pic_url] = like_ct
        
        return like

    def Statistic(self, like):
        try:
            # Transform "like" dict format from [picture url:likes count] to [likes count:picture url]
            TransLike = {v : k for k, v in like.items()}
            # Get the most likes post
            Most_Liked_Posts = TransLike[max(like.values())]
        except:
            # Raise the exception to Run.py log.
            raise
            return
        
        return Most_Liked_Posts
    
    def SaveImage(self, img, account):
        # Save the most likes post picture
        img_path = os.path.join("C:/Users/m4104/Desktop/InstagramBot-project/mostlike/"+account)        
        urlretrieve(img, img_path + ".png")
    
    def check_pic(self, pic_url):
        sql = "SELECT * FROM instagram.mostlike WHERE url = (%s);"
        val = (pic_url,)
        self.cur.execute(sql,val)

        return self.cur.fetchall()
    
    def check_name(self, name):
        sql = "SELECT * FROM instagram.mostlike WHERE name = (%s);"
        val = (name,)
        self.cur.execute(sql,val)

        return self.cur.fetchall()
    
    def UpdateSQL(self, pic_url, name, likes_ct):
        if self.check_pic(Most_Liked_Posts) and self.check_name(name):
            print(1)
            return
        print(self.check_pic(Most_Liked_Posts))
        print(self.check_name(name))
        #elif (not self.check_pic(Most_Liked_Posts)) and self.check_name(name):
        #    print(2)
        #    sql = "UPDATE instagram.mostlike SET (url,name,likes) = (%s,%s,%s);"
        #else:
        #    print(3)
        #    sql = "INSERT INTO instagram.mostlike (url,name,likes) VALUES (%s,%s,%s);"
        #val = (pic_url, name, likes_ct)
        #self.cur.execute(sql,val)            
        #self.conn.commit()
        
    def close(self):
        self.conn.close()
    
    def Run(self, account="ID"):
        like = self.ProInfo(self.script)
        Most_Liked_Posts = self.Statistic(like)
        self.SaveImage(Most_Liked_Posts, account)
        self.UpdateSQL(Most_Liked_Posts, account, like[Most_Liked_Posts])
        
        return like[Most_Liked_Posts]

if __name__ == '__main__':
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    
    Crawler = Crawler(url)
    followers, followed, article = Crawler.RE(Crawler.script)
    Most_Liked_Posts  = Crawler.Run(ID)