"""
Module for fetching Telegram chat contents.
"""

from telethon import TelegramClient
from typing import Any, List, Tuple, Union, Sequence
from telethon.helpers import TotalList
import json
import os

def save_chat_ids(path="~/.config/tele_chat_ids.json"):

    # 1. Check file existing
    filename = os.path.expanduser(path)
    if not os.path.exists(filename):
        print(f"\033[34mFirst runnning, touching config files...\033[0m")
        chat_ids = []
    
    # 2. File exists, ask user
    else:
        print(f"\033[34mOld id config file found at {filename}, please select an option\033[0m")
        print("1. Create a new one")
        print("2. Keep old chat ID config")
        print("3. Append new ID into config")

        while True:
            choice = input("Please enter (1/2/3)").strip()
            if choice in ("1", "2", "3"):
                break 
            print("Invalid input, please enter again:")

        if choice == "1":
            print("Select: Create a new one and clean old config file")
            chat_ids = []
        elif choice == "2":
            print("Select: Keep old chat ID config")
            return
        else:
            print("Select: Append new ID into config")
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    chat_ids = json.load(f)
                    if not isinstance(chat_ids, list):
                        print("Warning: Origin config is not a list, a new config file will be created")
                        chat_ids = []
            except Exception:
                print("Warning: Can't read origin config file, a new one will be touched")
                chat_ids = []
    print("Please enter chat ID(enter one at a time, press Enter to finish typing)")
    while True:
        s = input(">").strip()
        if s == "":
            break
        try:
            chat_ids.append(int(s))
        except ValueError:
            print("Invalid ID, please enter again!")
            continue
        print(f"Add: {s}")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_ids, f, ensure_ascii=False, indent=4)
        print(f"\nSave complete, total IDs:{len(chat_ids)}")

async def fetch_chat_messages(
    client: TelegramClient,
    chat_entitys: List[Any],
    limit: int = 100
):
    
    print(f"\nFetching last {limit} messages...")
    messages = []
    msg_cluster = []
    chat_names = []
    for single_chat in chat_entitys:
        messages = await client.get_messages(single_chat, limit=limit) 
        assert isinstance(messages, TotalList)
        if not messages:
            print(f"No messages found in {single_chat.name}")
            continue
        msg_cluster.append(messages)

        print(f"\n{'='*80}")
        try:
            single_chat_name = getattr(single_chat, 'title', None) or getattr(single_chat, 'name', 'Unknown')
            chat_names.append(single_chat_name)
            print(f"Chat name \"{single_chat_name}\"")
            print(f"Message send time: {messages[0].date}")
            print(f"Newest message: \n{messages[0].text}") # type: ignore
            #sender = await client.get_entity(messages[0].sender_id)
            #if hasattr(sender, 'first_name'):
            #    print(f"\033[34mMessage sender: {sender.first_name}\033[0m") #type: ignore
        except ValueError:
            print("!!!Messages sequence is empty!!!")
        
        print(f"{'='*80}")
        print(f"Total messages fetched: {len(messages)}")  # type: ignore
    
    return msg_cluster, chat_names


async def select_and_fetch_chat(
    client: TelegramClient,
    dialogs: List[Any],
    limit: int = 100,
    path = "~/.config/tele_chat_ids.json"
):

    # Display all dialogs
    for d in dialogs:
        print(f"Title: {d.name} | ID: {d.id} | entity: {d.entity.__class__.__name__}")
    
    save_chat_ids(path=path)
    filename = os.path.expanduser(path)
    with open(filename, "r", encoding="utf-8") as f:
        entity_ids = json.load(f)

    select_chat = []
    for i in range(len(entity_ids)):
        for j in range(len(dialogs)):
            if dialogs[j].id == entity_ids[i]:
                select_chat.append(dialogs[j].entity)
                print(f"Found chat: {select_chat[-1].title}")
    
    
    if len(select_chat) == 0:
        raise ValueError(f"Chat with ID {entity_ids} not found in your dialogs. Please check the ID or use @username")
    
    # Fetch and display messages
    messages, chat_names = await fetch_chat_messages(client, select_chat, limit=limit)
    
    
    return messages, chat_names
