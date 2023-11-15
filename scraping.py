import requests
from bs4 import BeautifulSoup
from pyppeteer import launch

AMAZON_BASE_URL="https://www.amazon.fr"

async def search(search_query, search_results):
    base_url = AMAZON_BASE_URL + "/s"

    try:
        browser = await launch(options={'args': ['--no-sandbox']})
        page = await browser.newPage()

        await page.setExtraHTTPHeaders({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        })

        await page.goto(f'{base_url}?k={search_query}')

        await page.waitForSelector(".s-main-slot")

        content = await page.content()

        await browser.close()
    except Exception as e:
        print(f"Error occured when requesting page : {e}")
        return None


    # message=""
    # base_url = AMAZON_BASE_URL + "/s"
    # headers = {"User-Agent": "Mozilla 5.0"}
    # params = {"k": search_query}

    # page = requests.get(base_url, headers=headers, params=params)

    # if page.status_code != 200 and page.status_code != 301:
    #     return "Not found " + str(page.status_code)
    
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all(lambda tag: tag.name == "div" and tag.get("data-asin", '') != "" and not "AdHolder" in tag.get("class", ""))[:15]

    number = 1
    for result in results:
        title = result.find("span", {"class": "a-text-normal"})
        price = result.find("span", {"class": "a-offscreen"})
        link = result.find('a', {"class": "a-link-normal"}, href=True)

        if title and price and link:
            search_results.append({"title": title.text.strip(), "price": price.text.strip(), "link": AMAZON_BASE_URL + link['href']})
            message += str(number) + ". " + title.text.strip() + " - " + price.text.strip() + "\n"
            number += 1
        if number > 5:
            break
    return message


def get_price(url):
    headers = {'User-Agent': 'Mozilla 5.0'}
    page = requests.get(url, headers=headers)

    if page.status_code != 200 and page.status_code != 301:
        return "Not found " + str(page.status_code)

    soup = BeautifulSoup(page.content, "html.parser")
    price_int = soup.find(class_="a-price-whole")
    price_dec = soup.find(class_="a-price-fraction")

    if price_int is None or price_dec is None:
        return "Price not found " + str(page.status_code)
    return price_int.get_text() + price_dec.get_text() + '€'
