import pprint
import requests
import bs4


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
result = []
HEADERS = {'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
          'Accept-Language': 'ru-RU,ru;q=0.9',
          'Sec-Fetch-Dest': 'document',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-User': '?1',
          'Cache-Control': 'max-age=0',
          'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
          'sec-ch-ua-mobile': '?0'
}

res = requests.get('https://habr.com/ru/all/', headers=HEADERS)
res.raise_for_status()
text = res.text


print(f"Keywords = {KEYWORDS}")
add_keywords = input('Хотите добавить keyword (да/нет): ')

while add_keywords.lower() == 'да':
    keyword = input('Введите keyword: ')
    KEYWORDS.append(keyword)
    add_keywords = input('Хотите добавить keyword (да/нет): ')

print(f"Окончательные Keywords - {KEYWORDS}")

soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.find_all('article')

for article in articles:
    hubs = []
    title = article.find('h2')
    a_tag = title.find('a')
    href = a_tag.attrs['href']
    url = 'https://habr.com' + href    
    title_text = title.text
    title_hubs = article.find_all(class_="tm-article-snippet__hubs-item-link")
    for hub in title_hubs:
        hub_span = hub.find('span')
        hubs.append(hub_span.text)
    content = article.find(class_="tm-article-body")
    content_p = content.find_all('p')
    body = ''
    for p in content_p:
        body += p.text
    body
    for key in KEYWORDS:
        if title_text.lower().find(key) > -1 or body.lower().find(key) > -1 or hubs.count(key) > 0:
            date_tag = article.find('time')
            date = date_tag.attrs['title']
            result_item = f"{date} - {title_text} - {url}"
            result.append(result_item)

print(result)