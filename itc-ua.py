import requests
from bs4 import BeautifulSoup
import json
import time

URL = 'https://itc.ua/techno/'
start_time = time.time()
main_request = requests.get(URL)
soup = BeautifulSoup(main_request.content, 'html.parser')
soup_articles = soup.find_all('h2', class_='entry-title')


all_urls = []
for i in soup_articles:
    all_urls.append(i.a['href'])

parsed_data = []
for each_url in all_urls:
    page = requests.get(each_url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    entry_header_div = page_soup.find_all('div', class_='entry-header')[0]
    entry_body_div = page_soup.find_all('div', class_='post-txt')[0]


    data = {
        'title': entry_header_div.h1.text.strip(),
        'time': entry_header_div.div.span.text[19:24],
        'date': entry_header_div.div.span.text[6:16],
        'author': entry_header_div.div.a.text,
        'img': entry_body_div.img['src'],
        'body': entry_body_div.text.replace('\n', ' ')
    }


with open('ict-ua.json', 'w') as f:
    json.dump(parsed_data, f, indent=4)
    print("The json file is created")
    expired_time = round(time.time() - start_time)
    print('Total time:', expired_time, 'seconds')