import MainCrawler, SubCrawler
import logging

def Run(url):

    Main_Crawler = MainCrawler.Crawler(url)
    print("----------------- Login -----------------")
    Main_Crawler.login()
    print("----------------- Follow -----------------")
    Main_Crawler.follow()
    print("----------------- Get follow -----------------")
    Main_Crawler.get_follow()
    print("----------------- Check follow -----------------")
    Main_Crawler.check_follow()
    print("----------------- Close Main Crawler-----------------")
    Main_Crawler.close()
    
    Sub_Crawler = SubCrawler.Crawler()
    
    for name in Main_Crawler.follow_name:
        try:
            Sub_Crawler.get_url(url + "/" + name)
            like = Sub_Crawler.ProInfo(Sub_Crawler.script)
            Most_Liked_Posts = Sub_Crawler.Statistic(like)
            Sub_Crawler.UpdateSQL(Most_Liked_Posts, name, like[Most_Liked_Posts])
        except:
            logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='a')
            logging.debug("Catch an exception.\n" + "name: " + name, exc_info=True)
            
    Sub_Crawler.close()
        
if __name__ == '__main__':
    url = "https://www.instagram.com"
    Run(url)
    # ToDo list
    # Post the picture of user most-liked picture.
    