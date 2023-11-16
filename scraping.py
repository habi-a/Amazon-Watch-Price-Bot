import requests
from bs4 import BeautifulSoup

user_agent_list = [
    "Opera/8.79.(Windows CE; zu-ZA) Presto/2.9.173 Version/10.00",
    "Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/531.8.7 (KHTML, like Gecko) Version/4.0 Safari/531.8.7",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2 like Mac OS X; gl-ES) AppleWebKit/532.1.3 (KHTML, like Gecko) Version/3.0.5 Mobile/8B118 Safari/6532.1.3",
    "Mozilla/5.0 (Android 4.4.4; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/15.0.853.0 Safari/532.0",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 10.0; Trident/5.1)",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/48.0.899.0 Safari/532.0",
    "Mozilla/5.0 (iPad; CPU iPad OS 6_1_6 like Mac OS X) AppleWebKit/534.0 (KHTML, like Gecko) CriOS/28.0.872.0 Mobile/74O760 Safari/534.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows 95; Trident/3.0)",
    "Mozilla/5.0 (iPad; CPU iPad OS 14_2 like Mac OS X) AppleWebKit/536.2 (KHTML, like Gecko) FxiOS/11.1r7108.0 Mobile/76T801 Safari/536.2",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_2 rv:4.0; cy-GB) AppleWebKit/532.29.5 (KHTML, like Gecko) Version/5.0 Safari/532.29.5"
]

def get_page(url, params={}):
    isCaptcha = True
    i = 0
    headers = {
        'User-Agent': user_agent_list[i],
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    ua_number = len(user_agent_list)
    while isCaptcha:
        page = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(page.content, "html.parser")
        if 'To discuss automated access to Amazon data' in str(soup) or 'captcha' in str(soup):
            i += 1
            if i >= ua_number:
                break
            headers['User-Agent'] = user_agent_list[i]
            print(f'\rBot has been detected... retrying ... use new identity: {i} ', end='', flush=True)
            continue
        else:
            print('Bot bypassed i:' + str(i))
            return soup
    print('No User Agent working found')
    return ""
