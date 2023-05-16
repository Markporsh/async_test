from typing import Callable

import aiohttp
from aiohttp import web

from parse import currency_amounts
from utils import log_request, correct_data


def check_request(func: Callable) -> Callable:
    async def wrapper(request: aiohttp.web.Request) -> web.Response:
        try:
            payload = await request.json()
        except Exception as error:
            log_request(request, f'Неверные данные {error}')
            return web.Response(text=f'Неверные данные', status=400)
        currency = correct_data(payload, currency_amounts, request)
        if currency is not True:
            return web.Response(
                text=f'валюта {currency} не найдена', status=400
            )
        return await func(request, payload)
    return wrapper
