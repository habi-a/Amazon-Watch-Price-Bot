SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

def convert_price_to_number(price):
    price_without_symbol = price.replace('€', '')
    price_with_point = price_without_symbol.replace(',', '.')
    return float(price_with_point)
