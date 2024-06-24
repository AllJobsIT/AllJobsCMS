import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

loop = asyncio.get_event_loop()


def create_bot():
    return Bot(token=os.getenv('API_KEY'), parse_mode=ParseMode.MARKDOWN_V2)


def create_dispatcher(bot, loop):
    dp = Dispatcher(loop=loop)
    return dp
