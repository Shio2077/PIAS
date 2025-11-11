from http import client
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
import json
import socks
import asyncio


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
    target_chat = config.get("target_chat")

    proxy_cfg = config.get("proxy")
    proxy = (socks.SOCKS5, proxy_cfg["hostname"], proxy_cfg["port"])

    if proxy_cfg:
        proxy = (proxy_cfg["scheme"], proxy_cfg["hostname"], proxy_cfg["port"])
    else:
        proxy = ([None], [None], [None])

    #client = TelegramClient("session_name", api_id, api_hash, proxy=proxy)
    client = TelegramClient('anon', api_id, api_hash, proxy=proxy)

    me = await client.get_me()
