from math import sin
from typing import List, Any
from datetime import datetime, timezone, timedelta, tzinfo
import pytz

def sel_chat_cont(
        msg_cluster: List[List],
        chat_names: List[Any]
) -> str:
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
    modifyed_tz = pytz.timezone('Asia/Hong_Kong')
    modifyed_time = utc_modify(now, modifyed_tz)

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
            msg_text += "\n\nChat name:<" + chat_names[chat_idx] + ">" + msg_text_temp
        chat_idx += 1

    if (msg_text == ""):
        msg_text += "There was no further news or messages during that period."
    else:
        msg_text = "Message time::" + modifyed_time.isoformat() + "\n" + msg_text
    print(msg_text)

    return msg_text

def utc_modify(dt: datetime, tz: tzinfo) -> datetime:
    return dt.astimezone(tz)