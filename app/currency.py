import asyncio
from abc import ABC, abstractmethod

update_rates = asyncio.Queue()
update_amounts = asyncio.Queue()

currency_rates = {'usd': 1, 'eur': 1, 'rub': 1}


class CurrencyApp(ABC):
    def __init__(self, supported_currencies: tuple) -> None:
        self.supported_currencies = supported_currencies

    @abstractmethod
    async def fetch_currency_rates(self):
        pass

    @abstractmethod
    async def start_rest_api(self):
        pass

    @abstractmethod
    async def update_amounts(self):
        pass
