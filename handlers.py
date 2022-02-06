from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher, Bot, executor, types
import keyboard
from bot import bot, dp
from bot import Nft, shutdown
from aiogram.dispatcher import FSMContext
from States import *


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Hello, before using, I recommend that you read the manual :)', reply_markup=keyboard.mainMenu)


@dp.message_handler(content_types='text', state=None)
async def cmd_start(msg: types.Message):
    if msg.text == '⚙ Settings':
        await bot.send_message(msg.from_user.id, f'''<b>
0 - Default
1 - Accountability
2 - Ambition
3 - Conviction
4 - Curiosity
5 - Empathy
6 - Gratitude
7 - Humility
8 - Kind Candor
9 - Kindness
10 - Optimist
11 - Patience
12 - Self-awareness
13 - Tenacity
14 - Special
</b>''')
        await msg.answer('Select attributes (Example: 1,2,3,14):')

        await States.attributes.set()

    elif msg.text == '📜 Manual':
        pass
    else:
        await bot.send_message(msg.from_user.id, 'Command Not Found')


@dp.message_handler(state=States.attributes)
async def attributes(msg: Message, state: FSMContext):
    attributes = msg.text
    await state.update_data({"attributes": attributes})
    await bot.send_message(msg.from_user.id, f'''<b>
0 - Default
1 - Bubble Gum
2 - Diamond
3 - Gold
4 - Hologram
5 - Lava
</b>''')
    await msg.answer('Select spectaculars (Example: 1,2,3,14):')
    await States.next()


@dp.message_handler(state=States.Spectaculars)
async def spectaculars(msg: Message, state: FSMContext):
    spectaculars = msg.text
    await state.update_data({"Spectaculars": spectaculars})
    await bot.send_message(msg.from_user.id, f'''<b>
0 - Default
1 - Black
2 - Caviar
3 - Champange
4 - Clear
5 - Emerald
6 - Fur
7 - Galaxy
8 - Gold
9 - Granite
10 - Marble
11 - Neon
12 - Pearl
13 - Rainbow
14 - Silver
15 - Wood
</b>''')
    await msg.answer('Select Token Frames (Example: 1,2,3,14):')
    await States.next()


@dp.message_handler(state=States.TokenFrames)
async def spectaculars(msg: Message, state: FSMContext):
    token_frame = msg.text
    await state.update_data({"TokenFrame": token_frame})
    data = await state.get_data()

    await shutdown(dp)
    Nft(data)



