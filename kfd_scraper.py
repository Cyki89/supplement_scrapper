import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

PRODUCER = 'KFD'

URL = 'https://sklep.kfd.pl/bialko-c-50.html?q=Waga-kg-0.1-1.1/Dost%C4%99pno%C5%9B%C4%87-Dost%C4%99pne&order=product.sales.desc'


WEIGHT_PATTERN = re.compile(r'[0-9]+\s?g')
UNIT_PATTERN = re.compile(r'g')
PRICE_PATTERN = re.compile(r'[0-9]+,?[0-9]+')


def get_kfd_data(url=URL):
    soup = get_soup(url)
    product_elements = get_product_elements(soup, 'product')

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
        if not 'wpc' in name:
            continue

        url = get_url(product)

        image = get_image(product)
        
        weight = get_weight(name, WEIGHT_PATTERN)
        
        price = get_price(product.select_one('span.price'), PRICE_PATTERN)
        old_price = get_price(product.select_one('span.regular-price'), PRICE_PATTERN)
        discount = get_price(product.select_one('span.discount-amount'), PRICE_PATTERN)

        price_standarized = get_standard_price(price, weight)

        product_data.append({
            'producer' : PRODUCER,
            'name': name.upper(),
            'weight': weight,
            'price': price,
            'old_price': old_price,
            'discount': discount,
            'price_standarized' : price_standarized,
            'image' : image,
            'url' : url,
            'date_added': date
        })

    return product_data


def get_url(product):
    return product.select_one('a.thumbnail.product-thumbnail')['href']


def get_image(product):
    return product.find('img')['data-src']


def get_name(product):
    img_url = product.find('img')['data-full-size-image-url']
    return img_url.split('/')[-1][:-4].replace('-', ' ')


def get_weight(name, weight_pattern):
    weight_with_unit = weight_pattern.search(name).group(0).replace(' ', '')
    if not weight_with_unit:
        return None
    
    weight = int(re.split(UNIT_PATTERN, weight_with_unit)[0])
    return weight if 'g' in weight_with_unit else weight * 1000


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
    data = get_kfd_data(URL)
    for product in data:
        print(product)