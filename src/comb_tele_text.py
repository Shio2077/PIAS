from typing import List, Any
import time

def cut_chat_cont(msg_cluster: List[List]):
    pass
    msg_text_list = []
    for single_chat in msg_cluster:
        for single_msg in single_chat:
            msg_text_list.append(single_msg.raw_text)