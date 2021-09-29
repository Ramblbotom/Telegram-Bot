import json
import requests

from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException("Такой валюты нет")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            return APIException("Такой валюты нет")

        if base_key == sym_key:
            raise APIException(F'Введены две одинаковые валюты')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)