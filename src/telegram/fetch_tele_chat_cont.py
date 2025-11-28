"""
Module for fetching Telegram chat contents.
"""

from telethon import TelegramClient
from typing import Any, List, Tuple, Union, Sequence
from telethon.helpers import TotalList
import json
import os, sys

def save_chat_ids(config_path="~/.config/telegram_config.json"):
    """
    Detect and manage the chat_ids field in telegram_config.json.
    - If chat_ids does not exist, prompt the user to enter new IDs
    - If chat_ids exists, allow the user to choose to keep or append new IDs
    The creation of the config file is the responsibility of the parent function.
    """
    filename = os.path.expanduser(config_path)
    
    # Read the config file (assumed to be created by the parent function)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to read config file {filename}: {e}")
    
    # Detect chat_ids field
    chat_ids = config.get("chat_ids", None)
    
    if chat_ids is None or (isinstance(chat_ids, list) and len(chat_ids) == 0):
        # chat_ids does not exist or is empty, prompt user to enter new IDs
        print("\033[34mNo chat IDs configured yet.\033[0m")
        print("Please enter chat IDs (press Enter to finish typing):")
        chat_ids = _input_chat_ids()
    else:
        # chat_ids exists and is not empty, let user choose
        print(f"\033[34mCurrent chat IDs: {chat_ids}\033[0m")
        print("1. Keep current config")
        print("2. Append new ID(s)")
        
        while True:
            choice = input("Please enter (1/2): ").strip()
            if choice in ("1", "2"):
                break
            print("Invalid input, please enter again:")
        
        if choice == "1":
            print("Select: Keep current chat ID config")
            return
        else:  # choice == "2"
            print("Select: Append new ID(s)")
            new_ids = _input_chat_ids()
            chat_ids.extend(new_ids)
            # Remove duplicates
            chat_ids = list(set(chat_ids))
    
    # Update chat_ids in config
    config["chat_ids"] = chat_ids
    
    # Save back to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    
    print(f"\n\033[32mSave complete!\033[0m")
    print(f"Total chat IDs: {len(chat_ids)}")
    print(f"IDs: {chat_ids}")


def _input_chat_ids(prompt="Enter chat ID (press Enter to finish): "):
    """
    Helper function: collect chat IDs from user input.
    """
    chat_ids = []
    while True:
        s = input(prompt).strip()
        if s == "":
            break
        try:
            chat_id = int(s)
            chat_ids.append(chat_id)
            print(f"Add: {chat_id}")
        except ValueError:
            print("Invalid ID format, please enter a valid integer!")
            continue
    return chat_ids

async def fetch_chat_messages(
    client: TelegramClient,
    chat_entitys: List[Any],
    limit: int = 100
):
    """
    Retrieving chat from the Telegram client
    Printing a portion of the chat content
    List msg_cluster stores all chat entities
    chat_names stores all chat names, in the same order as entities within msg_cluster
    """
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
        except ValueError:
            print("!!!Messages sequence is empty!!!")
        
        print(f"{'='*80}")
        print(f"Total messages fetched: {len(messages)}")  # type: ignore
    
    return msg_cluster, chat_names


async def select_and_fetch_chat(
    client: TelegramClient,
    dialogs: List[Any],
    limit: int = 100,
    config_path = "~/.config/telegram_config.json"
):
    """
    Select chats from dialogs based on chat_ids in telegram_config.json,
    then fetch and return their messages.
    """
    # Display all dialogs
    for d in dialogs:
        print(f"Title: {d.name} | ID: {d.id} | entity: {d.entity.__class__.__name__}")
    
    # Manage chat_ids
    save_chat_ids(config_path=config_path)
    
    # Read config file
    filename = os.path.expanduser(config_path)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to read config file: {e}")
    
    # Get chat_ids
    entity_ids = config.get("chat_ids", [])
    if not entity_ids:
        raise ValueError("No chat IDs found in config. Please run save_chat_ids first.")
    
    # Find corresponding entities from dialogs by ID
    select_chat = []
    for chat_id in entity_ids:
        found = False
        for dialog in dialogs:
            if dialog.id == chat_id:
                select_chat.append(dialog.entity)
                print(f"Found chat: {getattr(dialog.entity, 'title', getattr(dialog.entity, 'name', 'Unknown'))}")
                found = True
                break
        if not found:
            print(f"\033[33mWarning: Chat ID {chat_id} not found in dialogs, skipping.\033[0m")
    
    if len(select_chat) == 0:
        raise ValueError(f"No valid chats found from IDs: {entity_ids}")
    
    # Fetch and return messages
    messages, chat_names = await fetch_chat_messages(client, select_chat, limit=limit)
    
    return messages, chat_names
