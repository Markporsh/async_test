import json
import aiohttp
from aiohttp import web

from currency import update_rates, update_amounts, currency_rates
from decorators import check_request
from parse import currency_amounts
from utils import total_amount, log_request


async def get_usd(request: aiohttp.web.Request) -> web.Response:
    log_request(request, currency_amounts['usd'])
    return web.Response(text=str(currency_amounts['usd']))


async def get_eur(request: aiohttp.web.Request) -> web.Response:
    log_request(request, currency_amounts['eur'])
    return web.Response(text=str(currency_amounts['eur']))


async def get_rub(request: aiohttp.web.Request) -> web.Response:
    log_request(request, currency_amounts['rub'])
    return web.Response(text=str(currency_amounts['rub']))


async def get_amount(request: aiohttp.web.Request) -> web.Response:
    if not update_rates.empty():
        data = await update_rates.get()
        for value in data:
            currency_rates[value] = data[value]
        update_rates.task_done()
    response_data = {
        'usd': currency_amounts['usd'],
        'eur': currency_amounts['eur'],
        'rub': currency_amounts['rub'],
        'rub-usd': currency_rates['usd'],
        'rub-eur': currency_rates['eur'],
        'eur-usd': currency_rates['eur'] / currency_rates['usd'],
        'usd-amount': total_amount(currency_rates, currency_amounts, 'usd'),
        'eur-amount': total_amount(currency_rates, currency_amounts, 'eur'),
        'rub-amount': total_amount(currency_rates, currency_amounts, 'rub'),
    }
    log_request(request, response_data)
    return web.Response(text=json.dumps(response_data))


@check_request
async def set_amount(
        request: aiohttp.web.Request, payload: dict
) -> web.Response:
    for currency, amount in payload.items():
        currency = currency.lower()
        currency_amounts[currency] = amount

    log_request(request, 'Успешно изменено')
    await update_amounts.put(currency_amounts)
    return web.Response(text='Успешно изменено')


@check_request
async def modify_amount(
        request: aiohttp.web.Request, payload: dict
) -> web.Response:
    for currency, amount in payload.items():
        currency = currency.lower()
        if currency in currency_amounts:
            currency_amounts[currency] += amount

    log_request(request, 'Успешно изменено')
    await update_amounts.put(currency_amounts)
    return web.Response(text='Успешно изменено')
