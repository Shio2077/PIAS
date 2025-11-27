from math import sin
from typing import List, Any
from datetime import datetime, timezone, timedelta

def sel_chat_cont(
        msg_cluster: List[List],
        chat_names: List[Any]
):
    """
    过滤1分钟以外的消息文本
    将1分钟以内的文本拼接，达成以下文本效果：
    具体结构：
        聊天名1
        <发送者（如果有的话）>:文本1
        <发送者（如果有的话）>:文本2
        ...
        聊天名2
        <发送者（如果有的话）>:文本1
        <发送者（如果有的话）>:文本2
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

