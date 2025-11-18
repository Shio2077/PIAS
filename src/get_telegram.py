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

    for d in dialogs:
        print(f"Title: {d.name} | ID: {d.id} | entity: {d.entity.__class__.__name__}")

    select_chat = None
    entity_id = input("Enter chat or channel ID:")
    
    # Convert to integer for comparison
    try:
        entity_id = int(entity_id)
    except ValueError:
        raise ValueError(f"Invalid ID format: {entity_id}. Please enter a valid integer ID.")

    for d in dialogs:
        if d.id == entity_id:
            select_chat = d.entity
            break 

    if select_chat is None:
        raise ValueError(f"Chat with ID {entity_id} not found in your dialogs. Please check the ID or use @username")
    
    print(f"Found chat: {select_chat.title} ID = {select_chat.id}")
    
    print("\nFetching last 100 messages...")
    messages = await client.get_messages(select_chat, limit=100)  # type: ignore
    
    print(f"\n{'='*80}")
    print(f"Last 100 messages from: {select_chat.title}")
    print(f"{'='*80}\n")
    
    # Reverse to show from oldest to newest
    for msg in reversed(messages):  # type: ignore
        sender_name = "Unknown"
        if msg.sender_id:
            try:
                sender = await client.get_entity(msg.sender_id)
                # Handle different entity types
                if hasattr(sender, 'first_name'):  # User
                    sender_name = sender.first_name  # type: ignore
                elif hasattr(sender, 'title'):  # Chat or Channel
                    sender_name = sender.title  # type: ignore
            except:
                sender_name = f"ID: {msg.sender_id}"
        
        timestamp = msg.date.strftime("%Y-%m-%d %H:%M:%S") if msg.date else "Unknown time"
        text = msg.text if msg.text else "[Media or empty message]"
        
        print(f"[{timestamp}] {sender_name}: {text}")
    
    print(f"\n{'='*80}")
    print(f"Total messages fetched: {len(messages)}")  # type: ignore

if __name__ == "__main__":
    asyncio.run(main())