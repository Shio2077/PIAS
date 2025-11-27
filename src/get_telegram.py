from http import client
from pickle import TRUE
from pydoc import cli
from re import DEBUG
import select
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
import socks
import json
import asyncio
import time

# Import the chat content fetching functions
from fetch_tele_chat_cont import select_and_fetch_chat
from comb_tele_text import sel_chat_cont

debug = TRUE

def load_config():
    path = os.path.expanduser("~/.config/telegram_config.json")
    if not os.path.exists(path):
        raise FileExistsError(f"Config file not found:{path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
async def main():
    config = load_config()
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    target_chat = config["target_chat"]

    proxy_cfg = config.get("proxy")
    proxy = (socks.HTTP, proxy_cfg["hostname"], proxy_cfg["port"])
    if(debug):
        print("Read config")
        print(f"api_id = {api_id}")
        print(f"api_hash = {api_hash}")
        print(f"target chat: {target_chat}")
        print(f"Proxy setting - host: {proxy_cfg["hostname"]}, port: {proxy_cfg["port"]}")

    if proxy_cfg:
        scheme = proxy_cfg.get("scheme", "").lower()
        if scheme in ("socks5", "socks5h"):
            proxy = (socks.SOCKS5, proxy_cfg["hostname"], proxy_cfg["port"])
        elif scheme in ("socks4", "socks4a"):
            proxy = (socks.SOCKS4, proxy_cfg["hostname"], proxy_cfg["port"])
        else:
            proxy = (socks.HTTP, proxy_cfg["hostname"], proxy_cfg["port"])
        client = TelegramClient('anon', api_id, api_hash, proxy=proxy)
        print("Client will start with proxy")
    else:
        client = TelegramClient('anon', api_id, api_hash)
        print("Client will not start with proxy!")
    
    phone_number = config.get("phone_number")
    if not phone_number:
        raise ValueError("phone_number not found in config")
    
    await client.connect()
    if not await client.is_user_authorized():
        print("Client is not authorized")
        await client.send_code_request(phone_number)
        code = input('Enter the code: ')
        await client.sign_in(phone_number, code)
    
    await client.send_message('me', 'Hello from telethon!')

    print("Fetching your dialogs...")
    dialogs = await client.get_dialogs()

    # Use the imported function to select chat and fetch messages
    messages, chat_names = await select_and_fetch_chat(client, dialogs, limit=120)
    sel_chat_cont(messages, chat_names)

    print(f"{'='*80}")

    time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())