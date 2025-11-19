"""
Module for fetching Telegram chat contents.
"""

from telethon import TelegramClient
from typing import Any, List


async def fetch_chat_messages(
    client: TelegramClient,
    chat_entity: Any,
    limit: int = 100
) -> List[Any]:
    """
    Fetch messages from a chat/channel and print them to console.
    
    Args:
        client: Telethon TelegramClient instance (must be connected and authorized)
        chat_entity: The chat/channel entity to fetch messages from
        limit: Number of messages to fetch (default: 100)
    
    Returns:
        List of messages fetched
    
    Example:
        messages = await fetch_chat_messages(client, chat_entity, limit=100)
    """
    print(f"\nFetching last {limit} messages...")
    messages = await client.get_messages(chat_entity, limit=limit)  # type: ignore
    
    print(f"\n{'='*80}")
    print(f"Last {limit} messages from: {chat_entity.title}")
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
    select_chat = None
    entity_id = input("\nEnter chat or channel ID: ")
    
    # Convert to integer for comparison
    try:
        entity_id = int(entity_id)
    except ValueError:
        raise ValueError(f"Invalid ID format: {entity_id}. Please enter a valid integer ID.")
    
    # Find the selected chat
    for d in dialogs:
        if d.id == entity_id:
            select_chat = d.entity
            break 
    
    if select_chat is None:
        raise ValueError(f"Chat with ID {entity_id} not found in your dialogs. Please check the ID or use @username")
    
    print(f"\nFound chat: {select_chat.title} ID = {select_chat.id}")
    
    # Fetch and display messages
    messages = await fetch_chat_messages(client, select_chat, limit=limit)
    
    return messages
