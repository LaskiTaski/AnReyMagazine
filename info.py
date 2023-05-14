import requests
from bs4 import BeautifulSoup


def currency_info():
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}

    url = 'https://yandex.ru/search/?text=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D1%8F+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&lr=213'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    # info = soup.find('div', class_="ConverterHeader-Rate").text
    data = soup.find_all('div', class_="ConverterInput")[-1].find('input').\
        get('value').replace(',', '.')
    return float(data)

data = currency_info() +1.5
