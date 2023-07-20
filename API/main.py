import aiohttp
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from Bot.bot import BOT_TOKEN, BotClient, get_image_url
from celery import Celery


class Item(BaseModel):
    message: str


CHANNEL_ID = os.getenv("CHANNEL_ID")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")


bot = BotClient()
app = FastAPI()
celery = Celery("tasks", backend="redis://localhost:6379/0")
session = aiohttp.ClientSession()


@app.post("/send-message")
async def send_message_route(prompt: Item, request: Request):
    headers = {
        "Authorization": f"{CLIENT_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "type": 2,
        "application_id": "936929561302675456",
        "guild_id": f"{CHANNEL_ID}",
        "channel_id": f"{CHANNEL_ID}",
        "session_id": "effacc7b-e32c-4002-8f61-d4b471fe22c7",
        "data": {
            "version": "1118961510123847772",
            "id": "938956540159881230",
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "type": 3,
                    "name": "prompt",
                    "description": "What is the question?",
                    "required": True,
                    "value": f"{prompt.message}",
                }
            ],
        },
    }

    url = "https://discord.com/api/v9/interactions"
    
    async with session.post(url, headers=headers, json=data) as response:
        if response.status == 204:
            message = await response.json()
            message_id = message["id"]
            channel_id = message["channel_id"]
            await bot.wait_until_ready()
            bot.image_event.clear()
            bot.image_url = None
            await bot.wait_for("message", channel=channel_id, message_id=message_id, prompt=prompt.message)
            if bot.image_url:
                return {"image_url": bot.image_url}
            else:
                return {"message": "No image URL found"}
        else:
            return {"message": "Failed to send message to Discord API"}

