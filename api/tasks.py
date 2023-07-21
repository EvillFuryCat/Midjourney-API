import discord
import os
import requests
from celery import Celery
from redis import Redis


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")


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

redis = Redis(host="redis", port=6379, db=0)


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
                        "value": f"{prompt}",
                    }
                ],
            },
        }

        url = "https://discord.com/api/v9/interactions"

        with requests.Session() as session:
            response = session.post(url, headers=headers, json=data)
            response.raise_for_status()

    send_message()


@celery.task(bind=True)
def run_discord_bot(self, prompt):
    intents = discord.Intents.all()
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")

    @bot.event
    async def on_message(message: discord.Message):
        if message.author != bot.user:
            if prompt in message.content:
                if message.attachments:
                    for attachments in message.attachments:
                        image_url = attachments.url
                        if image_url:
                            redis.set(prompt, image_url)
                            await bot.close()

    # Start the Discord bot
    bot.run(BOT_TOKEN)