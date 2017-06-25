import requests
from bs4 import BeautifulSoup


def get_meta(pages=20):
    results = []
    for i in range(1, pages + 1):
        r = requests.post("http://www.mtgtop8.com/topcards", data={
            'data': 1,
            'current_page': i,
            'format': 'MO',
            'lands': 1,
            'maindeck': 'MD',
            'metagame_sel[MO]': 51,
        })

        soup = BeautifulSoup(r.text, 'html.parser')
        cards = [result.contents[1].text for result in soup.find_all(name='tr', class_='hover_tr') + soup.find_all(name='tr', class_='chosen_tr')]
        results += cards
    return results


with open('meta.txt', 'w') as meta:
    meta.writelines([card + '\n' for card in get_meta(10)])
