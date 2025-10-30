from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
import json
import asyncio


def load_config():
    path = os.path.expanduser("~/.config/telegram_config.json")
    if not os.path.exists(path):
        raise FileExistsError(f"Config file not found:{path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
async def main():
    config = load_config()