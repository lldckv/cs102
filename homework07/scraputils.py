import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    keys = ['author', 'comments', 'points', 'title', 'url']
    list1 = parser.table.findAll('tr', {'class': 'athing'})
    list2 = parser.table.findAll('td', {'class': 'subtext'})
    #f = lambda x: x if requests.get(x).status_code==200 else None
    for i in range(len(list1)):
        t = [
        ((lambda x: x if x is None else x.text)(list2[i].find('a', {'class': 'hnuser'}))),
        ((lambda x: int(x.split('\xa0')[0]) if 'comment' in x else None)(list2[i].findAll('a')[-1].text)),
        ((lambda x: x if x is None else int(x.text.split(' ')[0]))(list2[i].find('span', {'class': 'score'}))),
        (list1[i].find('span', {'class': 'titleline'}).a.text),
        (lambda x: 'https://news.ycombinator.com/'+x if x.startswith('item?id=') else x)((list1[i].find('span', {'class': 'titleline'}).a.get('href')))]
        #print(t[4])
        d = {keys[i]: t[i] for i in range(len(keys))}
        news_list.append(d)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    if parser.find('a', {'class': 'morelink'}) is None:
        if parser.find('span', {'class': 'hnmore'}) is not None:
            return parser.find('span', {'class': 'hnmore'}).a.get('href')
        else:
            return 'front'
    else:
        return parser.find('a', {'class': 'morelink'}).get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        extract_next_page(soup)
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
