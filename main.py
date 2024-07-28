import requests
from bs4 import BeautifulSoup
import pandas
import time, random
from pages import all_links_on_page, info_from_announcement, make_request

headers = {
    "Accept": "text/html",
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'u,en;q=0.9',
    'Content-Type': 'application/json',
    'Priority': 'u=1, i',
    'Sec-Ch-Ua': '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
    'Sec-Ch-Ua-Arch': '"x86"',
    'Sec-Ch-Ua-Bitness': '"64"',
    'Sec-Ch-Ua-Full-Version': '"24.6.0.1874"',
    'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="124.0.6367.71", "YaBrowser";v="24.6.0.1874", "Not-A.Brand";v="99.0.0.0", "Yowser";v="2.5"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Model': '""',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
    'sec-Fetch-Dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
}

all_data = []
counter = 0
session = requests.session()
session.headers = headers
for page in range(31, 54):
    url = f'https://saratov.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={page}&region=4969&room2=1'
    print(f'Parsing page number {page}')
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = all_links_on_page(soup)
        for link in links:
            response_of_announcement = make_request(link, headers)
            time.sleep(random.randint(4, 7) + random.random()*2)
            if response_of_announcement.status_code == 200:
                soup_of_announcement = BeautifulSoup(response_of_announcement.text, "html.parser")
                data = info_from_announcement(soup_of_announcement)
                if None in data.values():
                    pass
                else:
                    all_data.append(data)
                    print(all_data)
            else:
                print(f'Error of the access to the pages: {response_of_announcement.status_code}')
    else:
        print(f'Error of the access to the site: {response.status_code}')
    counter += 1
    if counter == 11:
        df = pandas.DataFrame(all_data)
        df.to_csv(f'output{page}.csv', index=False, encoding='utf-8')
        all_data = []
        counter = 0
    if page == 53:
        df = pandas.DataFrame(all_data)
        df.to_csv(f'output{page}.csv', index=False, encoding='utf-8')
        all_data = []
        counter = 0


session.close()
