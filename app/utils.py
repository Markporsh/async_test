import json
import logging

import aiohttp
from aiohttp import web


def total_amount(curses: dict, moneys: dict, currency: str) -> int:
    answer = 0
    for money in moneys:
        answer += moneys[money] * (curses[money] / curses[currency])

    return round(answer, 3)


def log_amounts(
        currency_amounts: dict,
        prev_money: dict,
        currency_rates: dict
) -> None:
    for cur, amount in currency_amounts.items():
        difference = amount - prev_money[cur]
        if difference != 0:
            logging.info(
                f'Изменение в накоплениях {cur} на {difference} '
                f'едениц. Валюты {cur} сейчас {amount}'
            )
        summ = total_amount(currency_rates, currency_amounts, cur)
        logging.info(f'Общая сумма {cur} на счету = {summ}')


def log_rates(
        currency_amounts: dict,
        prev_currency: dict,
        currency_rates: dict
) -> None:
    for cur, rate in currency_rates.items():
        difference = rate - prev_currency[cur]
        if difference != 0:
            logging.info(
                f'Измненен курс {cur} на {difference} пунктов, '
                f'курс сейчас - {rate}'
            )
        summ = total_amount(currency_rates, currency_amounts, cur)
        logging.info(f'Общая сумма {cur} на счету = {summ}')


def log_request(request: aiohttp.web.Request, response: str or dict):
    logging.debug(f'request - {request}')
    logging.debug(f'response - {response}')


def correct_data(
        payload: json,
        currency_amounts: dict,
        request: aiohttp.web.Request
) -> bool or str:
    for currency in payload:
        if currency not in currency_amounts:
            log_request(request, f'валюта {currency} не найдена')
            return currency
    return True
