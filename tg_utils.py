import requests
from bs4 import BeautifulSoup

def tg_getUpdates(tg_token, offset):
  url = 'https://api.telegram.org/bot' + tg_token + '/getUpdates?offset=' + str(offset)
  result_json = requests.get(url).json()
  return result_json

def tg_sendMessage(tg_token, chat_id, message):
  url = 'https://api.telegram.org/bot' + tg_token + '/sendMessage?chat_id=' + str(chat_id) + '&text=' + message + '&parse_mode=HTML'
  requests.get(url)

def tg_sendNews(tg_token, chat_id, news_cnt):
  news_url = 'https://wildrift.leagueoflegends.com/en-us/news/'
  news_result = requests.get(news_url)
  news_soup = BeautifulSoup(news_result.text)
  articles = news_soup.find_all('a', {'class' : 'articleCardWrapper-1JIOy '})

  for ind in range(news_cnt):
    article = articles[ind]
    article_url = article.get('href')
    if article_url[0] == '/':
      article_url = 'https://wildrift.leagueoflegends.com' + article_url

    print(ind)
    print(article_url)
    description = article.find('p').text
    print(description)
    name = article.find('h4').text
    print(name)
    date = article.find('span', {'class' : 'copy-01'}).text
    print(date)
    category = article.find('span', {'class' : 'copy-01 category-1WTtr'}).text
    print(category)

    line0 = '<i>' + date + '   ' + category + '</i>' + '\n'
    line1 = '<b>' + name[:-1] + '</b>' + '\n'
    line2 = description + '\n'
    line3 = '\n'
    line4 = article_url
    text = line0 + line1 + line2 + line3 + line4

    tg_sendMessage(tg_token, chat_id, text)
