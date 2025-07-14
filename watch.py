import asyncio

from amazon import get_price
from utils import convert_price_to_number, HOUR

async def watch_background(bot, watch_list):
    while True:
        await asyncio.sleep(12 * HOUR)
        for item in watch_list:
            message = ""
            price_today = get_price(item["link"])
            price_today_float = convert_price_to_number(price_today)
            price_stored_float = convert_price_to_number(item["price"])

            if (price_today_float != price_stored_float):
                message = "Price for: " + item["title"] + " has changed\n"
                message += "Old price: " + item["price"] + "\t New price: " + price_today
                item["price"] = price_today
                user = bot.get_user(item["user_id"])
                if user:
                    await user.send(message)
                else:
                    print("no user found to send alert")
