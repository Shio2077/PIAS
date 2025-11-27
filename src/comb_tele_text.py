from math import sin
from typing import List, Any
from datetime import datetime, timezone, timedelta

def sel_chat_cont(
        msg_cluster: List[List],
        chat_names: List[Any]
):
    """
    Filter message text older than 1 minute.
    Concatenate text from messages within 1 minute to achieve the following text effect:
    Specific structure:
    Chat name 1
    <Sender (if any)>: Text 1
    <Sender (if any)>: Text 2
    ...
    Chat name 2
    <Sender (if any)>: Text 1
    <Sender (if any)>: Text 2
    ...
    """
    msg_text = ""
    chat_idx = 0
    now = datetime.now(timezone.utc)
    for single_chat in msg_cluster:
        msg_text_temp = ""
        for single_msg in single_chat:
            diff = now - single_msg.date
            if diff <= timedelta(minutes=2):
                if (not hasattr(single_msg.sender, 'title')):
                    first_name = single_msg.sender.first_name or ""
                    username = single_msg.sender.username or ""
                    msg_text_temp = msg_text_temp + "\nUser<" + first_name + username + ">:" + single_msg.raw_text
                else:
                    msg_text_temp = msg_text_temp + "\nChannel message:" +single_msg.raw_text
        if (msg_text_temp != ""):
            #there is no new message in the chat
            msg_text += "\n\nGroup or channel:<" + chat_names[chat_idx] + ">" + msg_text_temp
        chat_idx += 1
    print(msg_text)

