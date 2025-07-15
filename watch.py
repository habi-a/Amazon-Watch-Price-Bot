import asyncio

from amazon import get_price
from utils import convert_price_to_number, HOUR

async def watch_background(bot, watch_list):
    while True:
        await asyncio.sleep(12 * HOUR)
        for user_id, items in watch_list.items():
            for item in items:
                price_today = get_price(item["link"])
                price_today_float = convert_price_to_number(price_today)
                price_stored_float = convert_price_to_number(item["price"])
                if price_today_float != price_stored_float:
                    item["price"] = price_today
                    user = await bot.fetch_user(item["user_id"])
                    if user:
                        await user.send(
                            f"Prix modifié pour **{item['title']}**\n"
                            f"Ancien prix : {item['price']}\n"
                            f"Nouveau prix : {price_today}"
                        )
                    else:
                        print(f"Impossible d’envoyer un message à l’utilisateur {item.get('user_id')}")
