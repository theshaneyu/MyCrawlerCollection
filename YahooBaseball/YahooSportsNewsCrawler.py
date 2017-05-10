import requests, json
from bs4 import BeautifulSoup

class SportsNews(object):
    def __init__(self):
        self.news_url = 'https://tw.news.yahoo.com'


    def get_species_res(self):
        """
        INPUT : none
        
        OUTPUT : the pages of different sport species (in a list)
        
        INFORMATION:
        get_species_res() returns a list of the responses of
        all kinds of sports page on yahoo news
        """
        sports_species = ['baseball', 'basketball', 'golf', 'tennis', 'other-sports']
        species_list = list()
        for item in sports_species:
            try:
                res = requests.get(self.news_url + '/' + str(item) + '/')
                species_list.append(res.text)
            except Exception as e:
                print(e)
        
        return species_list


    def species_news(self, species_page):
        """
        INPUT : result from get_species_res()
        OUTPUT : news_content_list
    
        INFORMATION :
        species_news first get the list of all the links of every species' news, 
        then secondly do the get() request to every single link
        """
        spec_count = 1
        count = 1

        news_link_list = list()
        news_content_list = list()

        for p in species_page: # 每個p是一個類別頁面
            soup = BeautifulSoup(p, 'html.parser')
            for a in soup.select('li.list-story > div > a'): # 迴圈一次塞一個p頁面的所有<a>link
                news_link_list.append(self.news_url + a['href']) # news_link_list checked

            print('第' + str(spec_count) + '個種類的連結已掛完')
            spec_count += 1

        for item in news_link_list:
            try:
                res = requests.get(item)
            except:
                continue
            news_content_list.append(res.text)
            print('第' + str(count) + '篇新聞已爬完')
            count += 1

        return news_content_list


    def single_content(self, spec_content_list):
        article_long_string = ''

        for article in spec_content_list:
            inner_soup = BeautifulSoup(article, 'html.parser')
            article_contents = inner_soup.find_all('div', {'itemtype':'https://schema.org/Article'})
            for item in article_contents:
                article_long_string += item.get_text() + '-------'

        return article_long_string


    def str_processing(self, long_string):
        without_break = long_string.replace('\n', '')
        break_between_articles = without_break.replace('-------', '\n')
        # return break_between_articles
        return break_between_articles


    def main(self):
        spec_list = self.get_species_res()
        print('=====所有種類的頁面已爬完=====')
        contents_list = self.species_news(spec_list)
        print('=====所有單一的頁面已爬完=====')
        String = self.single_content(contents_list)
        print('=====所有單一頁面的文章內容已萃取完成=====')
        final_result = self.str_processing(String)

        with open('sport_news.txt', 'w') as f:
            f.write(final_result)

        print('=====寫檔完成=====')





if __name__ == '__main__':
    sport = SportsNews()
    sport.main()

