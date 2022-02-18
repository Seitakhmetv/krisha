from time import time
from bs4 import BeautifulSoup
import requests
import time

def card_url(page):
    page_url = "https://krisha.kz/prodazha/kvartiry/almaty/?page=" + str(page);
    page_html = requests.get(page_url).text

    soup = BeautifulSoup(page_html, "html.parser")

    card = soup.find_all('div', class_="a-card")

    card_link = []
    for i in range(len(card)):
        id = card[i].find("div", class_="a-card__header-left").a['href'].split("/")[3]
        url = "https://krisha.kz" + card[i].find("div", class_="a-card__header-left").a['href']
        card_link.append({"id": id, "url": url})
    return card_link

def card_parser(url):
    #card_url() => page_html
    page_html = requests.get(url).text
    soup = BeautifulSoup(page_html, "html.parser")
    
    sidebar = soup.find("div", class_='offer__sidebar')
    content = soup.find("div", class_='offer__content')

    title = soup.find("h1").text.replace("  ", "").replace("\n", "")
    price = sidebar.find(class_="offer__price").text.replace("  ", "").replace("\n", "").replace(u"\xa0", u" ")
    short_decr = sidebar.find_all(class_="offer__info-item")
    owner = sidebar.find(class_="owners__name").text.replace("  ", "").replace("\n", "")

    short_info = {}

    for i in short_decr:
        if("data-name" in i.attrs):
            short_info[i["data-name"]] = i.find(class_="offer__advert-short-info").text
        else:
            short_info["flat.city"] = i.find(class_="offer__location offer__advert-short-info").span.text
    
    house = {
        "title": title,
        "price": price,
        "owner": owner,
        "info": short_info,
        "page_url": url
    }
    return house

def main(page):
    links = card_url(page)
    parsed = []
    for link in links:
        parsed.append(str(card_parser(link['url'])))        
    return parsed

def parse_krisha():
    
    with open(f'result.txt', 'a', encoding="utf-8") as f:
        cnt = 0;
        for i in range(100, 1001):
            cnt += 1
            parsed = main(i)
            print("Start!!!")
            for parse in parsed:
                f.write(parse+"\n")
            print(f"page {i} has been parsed")
            
            if(cnt % 2 == 0):
                print("---timeout 2.5 minutes---")
                time.sleep(150)

def get_data():
    with open("result.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    data = set()
    cnt = 0;
    for line in lines:
        data.add(line)
    with open("newer_result.txt", "w", encoding="utf-8") as f:
        for i in data:
            f.write(i)

def compare():
    with open("result.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("newer_result.txt", "r", encoding="utf-8") as f:
        newer_lines = f.readlines()
    lines.sort()
    newer_lines.sort()
    for i in range(len(lines)):
        if(lines[i] != newer_lines[i]):
            print(lines[i])
compare()