import sys
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCER = 'BODY_PACK'

URL = 'https://www.bodypak.pl/pl/115-wpc-koncentraty-bialek-serwatkowych'


WEIGHT_PATTERN = re.compile(r'[1-9][0-9]+\s?g')
PRICE_PATTERN = re.compile(r'[0-9]+,?[0-9]+')


def get_bodypack_data(url=URL):
    soup = get_soup(url)
    product_elements = get_product_elements(soup, selector='li.ajax_block_product')

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
        if not weight or not 500 < weight < 1100:
            continue

        price = get_price(
            element=product.select_one('span.price'), 
            price_pattern = PRICE_PATTERN
        )

        old_price = get_price(
            element=product.select_one('span.old-price'), 
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
    return product.select_one('a.product-name')['title']


def get_url(product):
    return product.select_one('a.product-name')['href']


def get_image(product):
    return product.select_one('img')['data-original']


def get_weight(name, weight_pattern):
    weight = weight_pattern.search(name)
    return weight and int(weight.group(0)[:-1])


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
    data = get_bodypack_data(URL)

    for product in data:
        print(product)