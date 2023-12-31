import asyncio
import regex as re
from telethon import TelegramClient, events

api_id = 24308228  # ваш апи айди
api_hash = 'afcfde8b88be218303a7e2975bee8e63'  # ваш апи ключ

client = TelegramClient(session='session', api_id=api_id, api_hash=api_hash, system_version="4.16.30-vxSOSYNXA ")
client.start()

code_regex = re.compile(r"t\.me/(CryptoBot|send|tonRocketBot|CryptoTestnetBot|wallet|xrocket|tronsalebot)\?start=(CQ[A-Za-z0-9]{10}|C-[A-Za-z0-9]{10}|t_[A-Za-z0-9]{15}|[A-Za-z]{12})", re.IGNORECASE)

replace_chars = ''' @#&+()*"'…;,!№•—–·±<{>}†★‡„“”«»‚‘’‹›¡¿‽~`|√π÷×§∆\\°^%©®™✓₤$₼€₸₾₶฿₳₥₦₫₿¤₲₩₮¥₽₻₷₱₧£₨¢₠₣₢₺₵₡₹₴₯₰₪'''
translation = str.maketrans('', '', replace_chars)

crypto_black_list = [1622808649, 1559501630, 1985737506, 5014831088, 6014729293]

@client.on(events.MessageEdited(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
@client.on(events.NewMessage(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
async def handle_new_message(event):
    message_text = event.message.text.translate(translation)
    codes = code_regex.findall(message_text)
    if codes:
        for bot_name, code in codes:
            await client.send_message(bot_name, message=f'/start {code}')
    try:
        for row in event.message.reply_markup.rows:
            for button in row.buttons:
                try:
                    match = code_regex.search(button.url)
                    if match:
                        await client.send_message(match.group(1), message=f'/start {match.group(2)}')
                except AttributeError:
                    pass
    except AttributeError:
        pass

client.run_until_disconnected()
