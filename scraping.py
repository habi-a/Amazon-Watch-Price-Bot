import requests
from bs4 import BeautifulSoup


def get_price(url):
    headers = {'User-Agent': 'Mozilla 5.0'}
    page = requests.get(url, headers=headers)

    if page.status_code != 200:
        print("Error status code: " + str(page.status_code))
        return "Not found"

    soup = BeautifulSoup(page.content, "html.parser")

    price_int = soup.find(class_="a-price-whole")
    price_dec = soup.find(class_="a-price-fraction")

    if price_int is None or price_dec is None:
        return "Not found"
    return price_int.get_text() + price_dec.get_text() + '€'

def watch_price(url, price):
    headers = {'User-Agent': 'Mozilla 5.0'}
    page = requests.get(url, headers=headers)

    if page.status_code != 200:
        print("Error status code: " + str(page.status_code))
        return "Not found"

    soup = BeautifulSoup(page.content, "html.parser")

    price = soup.find(id="priceblock_ourprice", class_="a-size-medium a-color-price")

    return price.get_text()