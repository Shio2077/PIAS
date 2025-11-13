from http import client
from pickle import TRUE
from re import DEBUG
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
import socks
import json
import asyncio

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
    else:
        client = TelegramClient('anon', api_id, api_hash)

    #me = await client.get_me()

if __name__ == "__main__":
    asyncio.run(main())