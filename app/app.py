import asyncio
import json
import logging
import sys
import aiohttp

from parse import args_pars, currency_amounts
from aiohttp import web
from urls import urlpatterns
from currency import (
    CurrencyApp, update_rates,
    update_amounts, currency_rates
)
from utils import log_amounts, log_rates


class MyApp(CurrencyApp):

    def __init__(self, supported_currencies: tuple) -> None:
        super().__init__(supported_currencies)

    async def currency_changes(self, period: int) -> None:
        while True:
            rates = await self.fetch_currency_rates()
            for currency in currency_rates:
                if currency.upper() in rates['Valute']:
                    rate = rates['Valute'][currency.upper()]['Value']
                    currency_rates[currency] = rate
            await update_rates.put(currency_rates)
            await asyncio.sleep(period * 60)

    async def fetch_currency_rates(self) -> json:
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        try:
            con = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=con) as session:
                async with session.get(url) as response:
                    data = await response.text()
                    logging.info(f'Данные с сервера получены')
                    return json.loads(data)
        except Exception as error:
            logging.exception(f'Ошибка чтения курсов с сервера {error}')

    async def start_rest_api(self) -> None:
        runner = web.AppRunner(app)
        app.add_routes(routes=urlpatterns)
        try:
            await runner.setup()
            site = web.TCPSite(runner, 'localhost', 8080)
            await site.start()
        except Exception as error:
            logging.exception(f'Проблемы при запуске приложения {error}')
        else:
            logging.info('Приложение успешно запущено')

        while True:
            await asyncio.sleep(360)

    async def update_amounts(self) -> None:
        prev_money = currency_amounts.copy()
        prev_currency = currency_rates.copy()
        while True:
            if not update_amounts.empty():
                data = await update_amounts.get()
                for value in data:
                    currency_amounts[value] = data[value]
                update_amounts.task_done()
            if currency_amounts != prev_money:
                log_amounts(currency_amounts, prev_money, currency_rates)
                prev_money = currency_amounts.copy()
            if currency_rates != prev_currency:
                log_rates(currency_amounts, prev_currency, currency_rates)
                prev_currency = currency_rates.copy()
            await asyncio.sleep(60)


async def main() -> None:
    ap = MyApp(tuple(currency_amounts.keys()))
    tasks = []
    loop = asyncio.get_running_loop()
    tasks.append(loop.create_task(ap.currency_changes(args_pars.period)))
    tasks.append(loop.create_task(ap.update_amounts()))
    tasks.append(loop.create_task(ap.start_rest_api()))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    app = web.Application()
    log_level = logging.INFO
    if args_pars.debug and args_pars.debug.lower() in ['true', 1, 'y']:
        log_level = logging.DEBUG
    logging.basicConfig(stream=sys.stdout, level=log_level)
    asyncio.run(main())
