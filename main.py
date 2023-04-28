import aiohttp
import asyncio
import platform
import logging
from datetime import datetime


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                logging.error(f"Error status: {response.status} for {url}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f'Connection error: {url}: {e}')
        return None


async def get_exchange():
    return await request('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    current_datetime = datetime.now().strftime("%d.%m.%Y")
    result = []
    currency_list = {}
    currency = {}
    course = {}
    for i in asyncio.run(get_exchange()):
        for k, v in i.items():
            if k == "buy" or k == "sale":
                currency_list[k] = v
            elif v == "EUR" or v == "UAH":
                currency[v] = currency_list

        course[current_datetime] = currency
    result.append(course)
    print(result)