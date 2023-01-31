import requests
from bs4 import BeautifulSoup
import json
import time


start_time = time.time()
url = 'https://itc.ua/techno/'
print('Collecting data in progress... Please wait to the end')
main_request = requests.get(url)
soup = BeautifulSoup(main_request.content, 'html.parser')
soup_articles = soup.find_all('h2', class_='entry-title')
soup_time_date = soup.find_all('time', class_='published')


# Forming list for 'URL'
def url_collecting():
    all_title_urls = []
    for i in soup_articles:
        all_title_urls.append(i.a['href'])
    return all_title_urls


url_collecting()


# Forming list for 'title'
def titles_collecting():
    all_titles = [i.text.strip() for i in soup_articles]
    return all_titles


titles_collecting()


# Forming list for 'img'
def img_collecting():
    all_img_temp = []
    all_img =[]
    for each_url in url_collecting():
        request_for_each_page = requests.get(each_url)
        article_soup = BeautifulSoup(request_for_each_page.content, 'html.parser')
        soup_page_text = article_soup.find_all('div', class_='post-txt')
        for element in soup_page_text:
            all_img_temp.append(element.a['href'])
            all_img = [word for i, word in enumerate(all_img_temp) if i % 2 == 0]
    return all_img


img_collecting()


# Forming list for 'date'
def dates_collecting():
    all_dates = [i.text.strip()[0:10] for i in soup_time_date]
    return all_dates


dates_collecting()


# Forming list for 'author'
def authors_collecting():
    all_authors = []
    for one_url in url_collecting():
        request_on_page = requests.get(one_url)
        text_soup = BeautifulSoup(request_on_page.content, 'html.parser')
        page_text = text_soup.find_all('span', class_='vcard')

        for one_element in page_text:
            all_authors.append(one_element.a['title'][7:])
    return all_authors


authors_collecting()


# Forming list for 'time'
def time_collecting():
    all_time = [i.text.strip()[13:18] for i in soup_time_date]
    return all_time


time_collecting()


# Forming list for 'body'
def main_text_and_collecting():
    all_text_body = []
    for each_url in url_collecting():
        request_for_each_page = requests.get(each_url)
        article_soup = BeautifulSoup(request_for_each_page.content, 'html.parser')
        useless_classes = ['news-little-center', 'last-news-new', 'theme-day', 'wp-embedded-content', 'widget-title','row']
        soup_page_text = article_soup.find_all('div', class_='post-txt', attrs={'class': lambda x: all(i not in x for i in useless_classes)})
        for element in soup_page_text[:-1]:
            all_text_body.append(element.text.replace('\n', ''))
    return all_text_body


main_text_and_collecting()


# Forming a JSON
data_example_format = {
    'url': '',
    'title': '',
    'img': '',
    'body': '',
    'author': '',
    'date': '',
    'time': ''
}

with open('ict-ua.json', 'w') as f:
    parsed_data = [dict(zip(data_example_format.keys(), item)) for item in zip(url_collecting(), titles_collecting(), img_collecting(), main_text_and_collecting(), authors_collecting(), dates_collecting(), time_collecting())]
    json.dump(parsed_data, f, indent=4)
    print("The json file is created")
    expired_time = round(time.time() - start_time)
    print('Total time:', expired_time, 'seconds')