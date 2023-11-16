import requests
from bs4 import BeautifulSoup
from faker import Faker


def get_page(url, params={}):
    fake = Faker()
    uag_random = fake.user_agent()

    headers = {
        'User-Agent': uag_random,
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    isCaptcha = True
    while isCaptcha:
        page = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(page.content, "html.parser")
        if 'To discuss automated access to Amazon data' in str(soup) or 'captcha' in str(soup):
            uag_random = fake.user_agent()
            print(f'\rBot has been detected... retrying ... use new identity: {uag_random} ', end='', flush=True)
            continue
        else:
            print('Bot bypassed')
            return soup
