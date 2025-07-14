from scraping import get_page

AMAZON_BASE_URL="https://www.amazon.fr"


def search(search_query):
    message = ""
    results_list = []

    base_url = AMAZON_BASE_URL + "/s"
    params = {"k": search_query}
    soup = get_page(base_url, params)

    results = soup.find_all(
        lambda tag: tag.name == "div"
        and tag.get("data-asin")
        and "AdHolder" not in (tag.get("class") or [])
    )[:30]

    number = 1
    for result in results:
        h2_tag = result.find("h2")
        title_tag = h2_tag.find("span") if h2_tag else None
        price_tag = result.find("span", class_="a-offscreen")

        link_tag = result.find("a", class_="a-link-normal", href=True)

        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = link_tag["href"]
            if not link.startswith("http"):
                link = AMAZON_BASE_URL + link

            item = {
                "title": title,
                "price": price,
                "link": link
            }

            results_list.append(item)
            message += f"{number}. {title} - {price}\n"
            number += 1

        if number > 5:
            break

    return message, results_list


def get_price(url):
    soup = get_page(url)
    price_int = soup.find(class_="a-price-whole")
    price_dec = soup.find(class_="a-price-fraction")

    if price_int is None or price_dec is None:
        return "Price not found"
    return price_int.get_text() + price_dec.get_text() + '€'
