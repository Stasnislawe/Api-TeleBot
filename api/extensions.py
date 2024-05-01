import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Вы ввели две одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base_ticker}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote_ticker}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Вы ввели не правильное значение {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        priceonlyodnogo = json.loads(r.content)[keys[quote]]

        return priceonlyodnogo