import sys
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCER = 'OLIMP'

URL = 'https://olimpstore.pl/produkty/odzywki-i-suplementy/wheyproteinconcentratewpc-600g-700g-720g-750g-900g?cat=4&product_list_limit=all'


WEIGHT_PATTERN = re.compile(r'[1-9][0-9]+\s?g')
PRICE_PATTERN = re.compile(r'[0-9]+,?[0-9]+')


def get_olimp_data(url=URL):
    soup = get_soup(url)
    product_elements = get_product_elements(soup, selector='div.products:not(.top-products) div.product-item-info')

    return get_product_data(product_elements)


def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        sys.exit()

    return BeautifulSoup(response.text, 'html.parser')


def get_product_elements(soup, selector):
    return soup.select(selector)

def get_product_data(product_elements):
    date = str(datetime.now().date())

    product_data = []
    for product in product_elements:
        name = get_name(product)

        url = get_url(product)
        
        image = get_image(product)

        weight = get_weight(name, WEIGHT_PATTERN)

        price = get_price(
            element=product.select_one('span[data-price-type="finalPrice"] > span.price'), 
            price_pattern = PRICE_PATTERN
        )
        old_price = get_price(
            element=product.select_one('span[data-price-type="oldPrice"] > span.price'), 
            price_pattern=PRICE_PATTERN
        )
        discount = get_discount(price, old_price)
        
        price_standarized = get_standard_price(price, weight)

        product_data.append({
            'producer' : PRODUCER,
            'name': name.upper(),
            'weight': weight,
            'price': price,
            'old_price': old_price,
            'discount': discount,
            'price_standarized' : price_standarized,
            'image': image,
            'url' : url,
            'date_added': date            
        })

    return product_data


def get_name(product):
    return product.select_one('a.product-item-link')['title']


def get_url(product):
    return product.select_one('a.product-item-link')['href']


def get_image(product):
    return product.find('img')['src']


def get_weight(name, weight_pattern):
    return int(weight_pattern.search(name).group(0)[:-1])


def get_price(element, price_pattern):       
    return (
        element and 
        float(price_pattern.search(element.text).group(0).replace(',', '.'))
    )

def get_discount(price, old_price):
    return old_price and round(old_price - price, 2)


def get_standard_price(price, weight):
    base_weight = 100
    
    return round(base_weight * price / weight, 2)


if __name__ == '__main__':
    data = get_olimp_data(URL)
    for product in data:
        print(product)


