import json
import os
from telegram import get_telegram
from gemini import gemini_summary
import asyncio
import threading

def setup_config():
    """
    在程序第一次启动时提供引导。
    如果是第一次启动：
        要求写入gemini api token
        要求写入telegram api token
        要求写入代理配置
    如果不是第一次启动：
        给出选项是否重新录入配置
        yes/no默认yes
    将telegram的所有相关信息保留在telegram_config.json
    将gemini的所有配置保留在gemini_config.json
    """
    pass

async def main():
    tele_msg_text = await get_telegram.get_messages()










if __name__ == "__main__":
    print("Hello, this is PIAS")
    asyncio.run(main())