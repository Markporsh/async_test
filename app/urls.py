from aiohttp import web
from views import (
    get_usd, get_amount, get_eur, get_rub,
    set_amount, modify_amount
)

urlpatterns = [
    web.get('/usd/get', get_usd),
    web.get('/rub/get', get_rub),
    web.get('/eur/get', get_eur),
    web.get('/amount/get', get_amount),
    web.post('/amount/set', set_amount),
    web.post('/modify', modify_amount),
]
