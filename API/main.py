import asyncio
import discord
import requests
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from celery import Celery
from redis import Redis


class Item(BaseModel):
    message: str


BOT_TOKEN = "MTEyODk3MTg4NjUwNDcxODM0Nw.GjdeFa.HiRVLZ-Ay_u6zI9nlQvUKdslfSl7ennSdby4Uw"
CHANNEL_ID = os.getenv("CHANNEL_ID")
CLIENT_TOKEN = (
    "MTEyNzg4MjI5NjcyNTM1MjQ0OA.GgLOki.U5mvD7FzXbLp9Bk85QibNOhh120pu39Ua119rM"
)


app = FastAPI()
celery = Celery(
    "tasks", broker="redis://127.0.0.1:6379/0", backend="redis://localhost:6379/0"
)

celery.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
)

redis = Redis(host="localhost", port=6379, db=0)


@celery.task(bind=True)
def send_message_to_discord(self, prompt: str):
    def send_message():
        headers = {
            "Authorization": f"{CLIENT_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        data = {
            "type": 2,
            "application_id": "936929561302675456",
            "guild_id": "285724843557781505",
            "channel_id": "285724843557781505",
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
                        "value": f"{prompt}",
                    }
                ],
            },
        }

        url = "https://discord.com/api/v9/interactions"

        with requests.Session() as session:
            response = session.post(url, headers=headers, json=data)
            if response.status_code == 204:
                # Start the discord bot task
                return True
            else:
                return False

    send_message()


@celery.task(bind=True)
def run_discord_bot(self, prompt):
    intents = discord.Intents.all()
    # Create a Discord bot client
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")

    @bot.event
    async def on_message(message: discord.Message):
        if message.author != bot.user:
            # Check if the message contains an image and matches the prompt
            if prompt in message.content:
                if message.attachments:
                    for attachments in message.attachments:
                        # Get the URL of the first attached image
                        image_url = attachments.url
                        if image_url:
                            # Stop the bot and return the image URL
                            redis.set(prompt, image_url)
                            await bot.close()

    # Start the Discord bot
    bot.run(BOT_TOKEN)


@app.post("/send-message")
async def send_message_route(prompt: Item, request: Request):
    message = prompt.message
    send_message_to_discord.delay(
        message
    )  # Start the Celery task to send message to Discord
    # Wait for the result of the Celery task
    run_discord_bot.delay(prompt.message)
    # Get the image URL from the Celery task result
    while True:
        image_url = redis.get(prompt.message)
        if image_url:
            image_url = image_url.decode("utf-8")
            break
        await asyncio.sleep(1)

    # Return the image URL
    return {"image_url": image_url}
