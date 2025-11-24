"""
Module for fetching Telegram chat contents.
"""

from email import message
from math import sin
from turtle import title
from telethon import TelegramClient
from typing import Any, List, Tuple, Union, Sequence
from telethon.helpers import TotalList
from telethon.tl.custom.message import Message

async def fetch_chat_messages(
    client: TelegramClient,
    chat_entitys: List[Any],
    limit: int = 100
) -> List[Any]:
    
    print(f"\nFetching last {limit} messages...")
    msg_idx = 0
    messages = []
    msg_cluster = []
    for single_chat in chat_entitys:
        messages = await client.get_messages(single_chat, limit=limit) 
        assert isinstance(messages, TotalList)
        if not messages:
            print(f"No messages found in {single_chat.name}")
            continue
        msg_cluster.append(messages)

        print(f"\n{'='*80}")
        try:
            print(f"Chat {getattr(single_chat, 'title', None) or getattr(single_chat, 'name', 'Unknown')}")
            print(f"{messages[-1].text}") # type: ignore
        except ValueError:
            print("!!!Message sequence is empty!!!")
        print(f"\n{'='*80}")
        sender = await client.get_entity(messages[-1].sender_id)
        try:
            if hasattr(sender, 'first_name'):
                sender_name = sender.first_name
            elif hasattr(sender, 'title'):
                sender_name = sender.title
        except:
            sender_name = f"ID:{message[-1].sender_id}"     

            #timestamp = messages[-1].date.strftime("%Y-%m-%d %H:%M:%S") if msg.date else "Unknown time"
            #text = messages[-1].text if msg.text else "[Media or empty message]"
            
            #print(f"[{timestamp}] {sender_name}: {text}")
        
        print(f"\n{'='*80}")
        print(f"Total messages fetched: {len(messages)}")  # type: ignore
    
    return msg_cluster


async def select_and_fetch_chat(
    client: TelegramClient,
    dialogs: List[Any],
    limit: int = 100
) -> List[Any]:
    """
    Interactive function to select a chat from dialogs and fetch its messages.
    
    Args:
        client: Telethon TelegramClient instance (must be connected and authorized)
        dialogs: List of dialog objects from client.get_dialogs()
        limit: Number of messages to fetch (default: 100)
    
    Returns:
        List of messages from the selected chat
    
    Example:
        dialogs = await client.get_dialogs()
        messages = await select_and_fetch_chat(client, dialogs, limit=100)
    """
    # Display all dialogs
    for d in dialogs:
        print(f"Title: {d.name} | ID: {d.id} | entity: {d.entity.__class__.__name__}")
    
    # Get user input for chat selection
    select_chat = []
    e_cnt = 0
    entity_ids = []
    while True:
        s = input("\nEnter chat or channel ID:")
        if (s == ""):
            break
        entity_ids.append(s)
    print("\nInput end, got ID list:", entity_ids)
    # Convert to integer for comparison
    try:
        entity_id = [int(eid) for eid in entity_ids]
    except ValueError:
        raise ValueError(f"Invalid ID format, please enter a valid integer ID.")
    
    for i in range(len(entity_id)):
        for j in range(len(dialogs)):
            if dialogs[j].id == entity_id[i]:
                select_chat.append(dialogs[j].entity)
                print(f"Found chat: {select_chat[-1].title}")
    
    
    if len(select_chat) == 0:
        raise ValueError(f"Chat with ID {entity_id} not found in your dialogs. Please check the ID or use @username")
    
    # Fetch and display messages
    messages = await fetch_chat_messages(client, select_chat, limit=limit)
    
    return messages
