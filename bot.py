import time
import datetime
from bs4 import BeautifulSoup
import requests
import lxml
import keyboard as nav
import re
import _thread
import json
import asyncio
import aiogram
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import keyboard
import handlers

with open('config.json', 'r') as config:
    cfg = json.loads(config.read())

loop = asyncio.new_event_loop()
bot = Bot(token=cfg[0]['TOKEN'], parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)


async def shutdown(dp):
    await storage.close()


class Nft:
    def __init__(self, data):
        self.static_attributes = ['Empathy', 'Accountability', 'Ambition', 'Conviction', 'Curiosity', 'Empathy', 'Gratitude', 'Humility', 'Kind Candor', 'Kindness', 'Optimist', 'Patience', 'Self-awareness', 'Tenacity', 'Special']
        self.static_spectaculars = ['Hologram', 'Bubble Gum', 'Diamond', 'Gold', 'Hologram', 'Lava']
        self.static_frames = ['Rainbow', 'Black', 'Caviar', 'Champange', 'Clear', 'Emerald', 'Fur', 'Galaxy', 'Gold', 'Granite', 'Marble', 'Neon', 'Pearl', 'Rainbow', 'Silver', 'Wood']

        self.multy_attributes = []
        self.multy_spectaculars = []
        self.multy_frames = []

        self.attributes_list = []
        self.spectaculars_list = []
        self.frames_list = []
        self.generated_url = []

        self.attributes = data['attributes'].split(sep=',', maxsplit=-1)
        self.spectaculars = data['Spectaculars'].split(sep=',', maxsplit=-1)
        self.frames = data['TokenFrame'].split(sep=',', maxsplit=-1)
        self.generate_url()

        with open('settings_name.txt', 'w') as save:
            for item in self.frames_list:
                save.write("%s\n" % item)
        with open('settings.txt', 'w') as save:
            for item in self.generated_url:
                save.write("%s\n" % item)
        self.send('updated')


    def generate_url(self):
        try:
            used = []
    #Generate Attributes
            for i in self.attributes:
                if i not in used:
                    used.append(i)
            for i, c in enumerate(used):
                if c.isnumeric():
                    self.attributes_list.append(self.static_attributes[int(c)])
            used = []
    #Generate Spectaculars
            for i in self.spectaculars:
                if i not in used:
                    used.append(i)
            for i, c in enumerate(used):
                if c.isnumeric():
                    self.spectaculars_list.append(self.static_spectaculars[int(c)])
            used = []
    #Generate Frames
            for i in self.frames:
                if i not in used:
                    used.append(i)
            for i, c in enumerate(used):
                if c.isnumeric():
                    self.frames_list.append(self.static_frames[int(c)])
            used = []

        except:
            type = 'range_out'
            self.send(type)

        self.count_attributes = len(self.attributes_list)
        self.count_spectacular = len(self.spectaculars_list)
        self.count_frames = len(self.frames_list)

        urls = []
        for i, c in enumerate(self.frames_list):
            for l, v in enumerate(self.spectaculars_list):
                for j, k in enumerate(self.attributes_list):
                    url = f'https://api.x.immutable.com/v1/orders?include_fees=true&status=active&sell_token_address=0xac98d8d1bb27a94e79fbf49198210240688bb1ed&sell_metadata=%7B%22Attribute%22%3A%5B%22{k.replace(" ", "%20")}%22%5D%2C%22Spectacular%22%3A%5B%22{v.replace(" ", "%20")}%22%5D%2C%22Token%20Frame%22%3A%5B%22{c.replace(" ", "%20")}%22%5D%7D&buy_token_type=ETH&order_by=buy_quantity&direction=asc&page_size=100'
                    urls.append(url)
            self.generated_url.append(urls)
            urls = []

    def send(self, type):
        global text
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if type == 'updated':
            text = f'''
<b>Updated Settings:)</b>
😋<b>Your Attributes</b> - <i>{self.attributes_list}</i>
🤯<b>Your Spectaculars</b> - <i>{self.spectaculars_list}</i>
🤤<b>Your Token Frames</b> - <i>{self.frames_list}</i>'''
        elif type == 'range_out':
            text = '<b>Pls, try again or read manual</b>'
        with open('config.json', 'r') as fp:
            cfg = json.loads(fp.read())

        for id in cfg[0]["id"]:
            url = f"https://api.telegram.org/bot{cfg[0]['TOKEN']}/sendMessage"
            data = {
                'chat_id': f'{id}',
                'text': f'{text}',
                'parse_mode': f'html'
            }
            requests.get(url, data=data)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=True, )

