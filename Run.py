import MainCrawler, SubCrawler
import logging

def Run(url):

    Main_Crawler = MainCrawler.Crawler(url)
    Main_Crawler.login()
    Main_Crawler.follow()
    Main_Crawler.get_follow()
    Main_Crawler.check_follow()
    Main_Crawler.close()
    
    for name in Main_Crawler.follow_name:
        try:
            Sub_Crawler = SubCrawler.Crawler(url + "/" + name)
            like = Sub_Crawler.ProInfo(Sub_Crawler.script)
            Most_Liked_Posts = Sub_Crawler.Statistic(like)
            Sub_Crawler.SaveImage(Most_Liked_Posts, name)
        except:
            logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a')
            logging.debug("Catch an exception.\n" + "name: " + name, exc_info=True)
        
if __name__ == '__main__':
    url = "https://www.instagram.com"
    Run(url)
    