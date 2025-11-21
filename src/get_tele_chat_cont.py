"""
Module for fetching Telegram chat contents.
"""

from email import message
from telethon import TelegramClient
from typing import Any, List, Tuple, Union, Sequence
from telethon.tl.types import User, Chat, Channel


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
        msg_cluster.append(messages)

        print(f"\n{'='*80}")
        print(f"Newest messages from: {single_chat.name} ") #type: ignore
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
    
    return messages


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
    entity_id = []
    while True:
        entity_id[e_cnt] = input("\nEnter chat or channel ID:")
        if (entity_id[e_cnt] == "\n"):
            break
        else:
            e_cnt = e_cnt + 1
    
    # Convert to integer for comparison
    try:
        entity_id = [int(eid) for eid in entity_id]
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
