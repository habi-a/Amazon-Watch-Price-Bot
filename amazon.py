from scraping import get_page

AMAZON_BASE_URL="https://www.amazon.fr"


def search(search_query, search_results):
    message=""
    base_url = AMAZON_BASE_URL + "/s"
    params = {"k": search_query}

    soup = get_page(base_url, params)
    results = soup.find_all(lambda tag: tag.name == "div" and tag.get("data-asin", '') != "" and not "AdHolder" in tag.get("class", ""))[:30]

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
    soup = get_page(url)
    price_int = soup.find(class_="a-price-whole")
    price_dec = soup.find(class_="a-price-fraction")

    if price_int is None or price_dec is None:
        return "Price not found"
    return price_int.get_text() + price_dec.get_text() + '€'