import json
import time
import datetime
from bs4 import BeautifulSoup
import requests
import lxml
import keyboard as nav
import re
import threading
import asyncio


def parse(all_urls, name):
    print(f'MY NAME - {name}')
    urls = re.findall("'(.+?)'", all_urls)

    #Generation floors
    all_floor = []
    good_urls = []
    if all_floor == []:
        for i, url in enumerate(urls):
            try:
                response = requests.get(url)
                if str(response.status_code) == '200':
                    data = response.json()
                    data_price = data['result'][0]['buy']['data']['quantity']
                    if len(data_price) == 18:
                        floor_price = f'0.{round(int(data_price), 3)}'
                    elif len(data_price) == 19:
                        first_num = data_price[0]
                        floor_price = f'{first_num}.{data_price[1:]}'
                    elif len(data_price) == 20:
                        first_num = data_price[:2]
                        floor_price = f'{first_num}.{data_price[2:]}'
                    elif len(data_price) == 21:
                        first_num = data_price[:3]
                        floor_price = f'{first_num}.{data_price[3:]}'
                    else:
                        continue
                    print(floor_price)
                    all_floor.append(floor_price)
                    good_urls.append(url)
            except:
                continue
    good = []
    updater = time.time()

    for i in urls:
        if i.__contains__(name):
            id = i
    if all_floor != []:
        while True:
            time.sleep(8)
            if time.time() - updater > 600:
                break
            for i, z_url in enumerate(good_urls):
                sub_name = re.search('Attribute%22%3A%5B%22(.+?)%22%5D%2C%22Spectacular', z_url).groups()[0]
                price = all_floor[i]
                floor_price = round(float(price), 3)
                url = z_url
                response = requests.get(url)
                if str(response.status_code) == '200':
                    data = response.json()
                else:
                    time.sleep(20)
                    continue
                try:
                    for i in data['result']:
                        id = i['order_id']
                        self_awa = i['sell']['data']["token_id"]
                        data_price = f"{i['buy']['data']['quantity']}"
                        me = i["timestamp"]
                        properties = i['sell']['data']["properties"]["image_url"]
                        if len(data_price) == 18:
                            price = f'0.{round(int(data_price), 3)}'
                        elif len(data_price) == 19:
                            first_num = data_price[:1]
                            price = f'{first_num}.{data_price[1:]}'
                        elif len(data_price) == 20:
                            first_num = data_price[:2]
                            price = f'{first_num}.{data_price[2:]}'
                        elif len(data_price) == 21:
                            first_num = data_price[:3]
                            price = f'{first_num}.{data_price[3:]}'
                        proc = ((float(price) - floor_price) / floor_price) * 100
                        if proc < 0:
                            spectacular_info = re.search(f':specials:book:(.+?):', properties).groups()[0]
                            print(f'Percent for {sub_name.replace("%20", " ")} + {spectacular_info.capitalize()} + {name}: {round(proc, 3)}')

                        url = f'https://tokentrove.com/collection/BookGames/imx-{id}'
                        if proc < cfg[0]["percentage"] and id not in already_sended:
                            spectacular_info = re.search(f':specials:book:(.+?):', properties).groups()[0].capitalize()
                            if spectacular_info == 'Bubble':
                                spectacular_info = 'Bubble%20Gum'
                            msg = ''
                            try:
                                msg += f'<b>PRICES</b>\n<i>Current Price -</i> <i>{round(float(price), 4)}</i>\n'
                                msg += f'<i>Floor Price -</i> <i>{floor_price}</i>\n'
                                msg += f'<i>Difference -</i> <b>{abs(round(proc, 4))}%</b>\n\n'
                                msg += f'''<b>FILTER - </b> <b>{spectacular_info.replace("%20", " ")} + {sub_name.replace("%20", " ")} + {name}</b>
<i>Self-awa -</i> <b>#{self_awa}</b>
<i>Attribute -</i> <i>{sub_name}</i>
<i>Spectacular -</i> <i>{spectacular_info.replace("%20", " ").upper()}</i>
<i>Frame -</i> <i>{name}</i>'''
                            except:
                                pass

                            send(url, msg, sub_name, spectacular_info, name)
                            good.append(f'{url}\n')
                            already_sended.append(id)

                except:
                    continue
                time.sleep(3)


def send(url, msg, sub_name, spectacular_info, name):
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'''
\n<b>🕗FAST CHECK:</b> <b>https://tokentrove.com/collection/BookGames?Attribute={sub_name.replace(" ", "%20")}&Spectacular={spectacular_info.replace(" ", "%20")}&Token%20Frame={name}&sort=price-asc</b>
\n💰<b>FAST BUY:</b> {url}
\n{msg}
                    '''

    url = f"https://api.telegram.org/bot{cfg[0]['TOKEN']}/sendMessage"
    for id in cfg[0]["id"]:
        data = {
            'chat_id': f'{id}',
            'text': f'{text}',
            'parse_mode': f'html',
            'disable_web_page_preview': True,
        }
        requests.get(url, data=data)


if __name__ == '__main__':
    with open('config.json', 'r') as fp:
        cfg = json.loads(fp.read())
    already_sended = []
    while True:
        with open('settings_name.txt', 'r') as fp:
            names = fp.readlines()

        with open('settings.txt', 'r') as fp:
            lines = fp.readlines()
            urls = fp.read()

#Generation threads
        threads = []
        try:
            q1 = threading.Thread(target=parse, args=(lines[0][:-1], names[0][:-1],))
            threads.append(q1)
        except:
            pass

        try:
            q2 = threading.Thread(target=parse, args=(lines[1][:-1], names[1][:-1],))
            threads.append(q2)
        except:
            pass

        try:
            q3 = threading.Thread(target=parse, args=(lines[2][:-1], names[2][:-1],))
            threads.append(q3)
        except:
            pass

        try:
            q4 = threading.Thread(target=parse, args=(lines[3][:-1], names[3][:-1],))
            threads.append(q4)
        except:
            pass

        try:
            q5 = threading.Thread(target=parse, args=(lines[4][:-1], names[4][:-1],))
            threads.append(q5)
        except:
            pass

        try:
            q6 = threading.Thread(target=parse, args=(lines[5][:-1], names[5][:-1],))
            threads.append(q6)
        except:
            pass

        try:
            q7 = threading.Thread(target=parse, args=(lines[6][:-1], names[6][:-1],))
            threads.append(q7)
        except:
            pass

        try:
            q8 = threading.Thread(target=parse, args=(lines[7][:-1], names[7][:-1],))
            threads.append(q8)
        except:
            pass

        try:
            q9 = threading.Thread(target=parse, args=(lines[8][:-1], names[8][:-1],))
            threads.append(q9)
        except:
            pass

        try:
            q10 = threading.Thread(target=parse, args=(lines[9][:-1], names[9][:-1],))
            threads.append(q10)
        except:
            pass

        try:
            q11 = threading.Thread(target=parse, args=(lines[10][:-1], names[10][:-1],))
            threads.append(q11)
        except:
            pass

        try:
            q12 = threading.Thread(target=parse, args=(lines[11][:-1], names[11][:-1],))
            threads.append(q12)
        except:
            pass

        try:
            q13 = threading.Thread(target=parse, args=(lines[12][:-1], names[12][:-1],))
            threads.append(q13)
        except:
            pass

        try:
            q14 = threading.Thread(target=parse, args=(lines[14][:-1], names[14][:-1],))
            threads.append(q14)
        except:
            pass

        works_thread = []
        for thread in threads:
            try:
                thread.start()
                works_thread.append(thread)
            except:
                pass

        for thread in works_thread:
            thread.join()

        print('10 min, reset')
        time.sleep(20)
