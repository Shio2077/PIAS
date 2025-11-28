from google import genai
from google.genai import types
import json
import os

async def load_config():
    pass


async def get_genai(api_key: str, prompt: str):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction=""
        )
    )
