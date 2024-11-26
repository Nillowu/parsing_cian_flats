import re
import time
import requests
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def make_request(url, headers):
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print(f"Trying again...")
            time.sleep(random.randint(50, 60) + random.random())
        else:
            return response


def remove_space(string_with_space):
    return re.sub(r'\s+', '', string_with_space)


def all_links_on_page(parsing_page):
    links = []
    for a_tag in parsing_page.find_all('a', class_='_93444fe79c--link--VtWj6'):
        link = a_tag.get('href')
        links.append(link)
    return links
def get_distance_from_centre(address_str):
    center_coords = (51.533008, 46.033978)
    geolocator = Nominatim(user_agent="real_estate_scraper")
    location = geolocator.geocode(address_str)
    if location:
        coords = (location.latitude, location.longitude)  # Получаем координаты
        distance_from_centre = geodesic(center_coords, coords).km  # Расстояние от центра города
        return round(distance_from_centre,3)
    else:
        return None


def info_from_announcement(parsing_link):
    address, distance_from_centre, year_of_construction, floor, kitchen_area, living_space, general_area, price = [], None, None, None, None, None, None, None
    for div in parsing_link.find_all('div', {'data-testid': 'price-amount'}):
        price = div.find('span', class_="a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_9u--limEs a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_28px--P1gR4 a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY").get_text(strip=True)
        price = (remove_space(price))
        price = price[:len(price)-1]
    for div in parsing_link.find_all('div', {'data-name': 'ObjectFactoidsItem'}):
        span = div.find('span', class_='a10a3f92e9--color_gray60_100--r_axa a10a3f92e9--lineHeight_4u--E1SPG a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_12px--pY5Xn a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5')
        if span and span.get_text(strip=True) == "Общая площадь":
            general_area = div.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').get_text(strip=True)
            general_area = (remove_space(general_area))
            general_area = general_area[:len(general_area) - 2]
        if span and span.get_text(strip=True) == "Жилая площадь":
            living_space = div.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').get_text(strip=True)
            living_space = (remove_space(living_space))
            living_space = living_space[:len(living_space) - 2]
        if span and span.get_text(strip=True) == "Площадь кухни":
            kitchen_area = div.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').get_text(strip=True)
            kitchen_area = (remove_space(kitchen_area))
            kitchen_area = kitchen_area[:len(kitchen_area) - 2]
        if span and span.get_text(strip=True) == "Этаж":
            floor = div.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').get_text(strip=True)
            floor = floor[0]
        if span and span.get_text(strip=True) == "Год постройки":
            year_of_construction = div.find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').get_text(strip=True)
    for a in parsing_link.find_all('a', class_= 'a10a3f92e9--address--SMU25'):
        part_address= a.get_text(strip=True)
        address.append(part_address)
    address=address[-2:]
    address_str = "Саратов, "+', '.join(address)
    data = {
        'price': price,
        'general_area': general_area,
        'living_space': living_space,
        'kitchen_area': kitchen_area,
        'floor': floor,
        'year_of_construction': year_of_construction,
        'distance_from_centre': get_distance_from_centre(address_str)
        }
    print(data)
    return data
