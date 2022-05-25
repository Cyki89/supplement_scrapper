import sys
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCER = 'SFD'

URL = 'https://sklep.sfd.pl/produkty.aspx?katid=119&c4=5&queryid=909abac83ed02aeefbb0ee2e7acacfbc'


NAME_SPLIT_PATTERN = re.compile(r'\r\n\s+')
WEIGHT_PATTERN = re.compile(r'[1-9][0-9]+g')
PRICE_PATTERN = re.compile(r'[0-9]+,?[0-9]+')


def get_sfd_data(url=URL):
    soup = get_soup(url)
    product_elements = get_product_elements(soup, 'products-list__box')
    
    return get_product_data(product_elements)


def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit()

    return BeautifulSoup(response.text, 'html.parser')


def get_product_elements(soup, cls_name):
    return soup.find_all(class_=cls_name)


def get_product_data(product_elements):
    date = str(datetime.now().date())
    
    product_data = []
    for product in product_elements:
        name = get_name(product)

        url = get_url(product)
        
        image = get_image(product)

        weight = get_weight(name, WEIGHT_PATTERN)

        price = get_price(product.select_one('span.cena'), PRICE_PATTERN)
        
        price_standarized = get_standard_price(price, weight)

        product_data.append({
            'producer' : PRODUCER,
            'name': name.upper(),
            'weight': weight,
            'price': price,
            'price_standarized' : price_standarized,
            'image': image,
            'url' : url,
            'date_added': date            
        })

    return product_data


def get_url(product):
    return f"https:{product.select_one('a.name')['href']}"


def get_image(product):
    return product.find('img')['src']


def get_name(product):
    return re.split(NAME_SPLIT_PATTERN, product.select_one('a.name').text)[-1]


def get_weight(name, weight_pattern):
    return int(weight_pattern.search(name).group(0)[:-1])


def get_price(element, price_pattern):       
    return (
        element and 
        float(price_pattern.search(element.text).group(0).replace(',', '.'))
    )


def get_standard_price(price, weight):
    base_weight = 100

    if not weight:
        return None
    
    return round(base_weight * price / weight, 2)


if __name__ == '__main__':
    data = get_sfd_data(URL)
    for product in data:
        print(product)