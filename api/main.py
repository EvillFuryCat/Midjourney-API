import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from api.tasks import run_discord_bot, send_message_to_discord, redis


class Item(BaseModel):
    message: str


app = FastAPI()


@app.post("/send-message")
async def send_message_route(prompt: Item):
    message = prompt.message
    send_message_to_discord.delay(
        message
    )
    run_discord_bot.delay(prompt.message)
    while True:
        image_url = redis.get(prompt.message)
        if image_url:
            image_url = image_url.decode("utf-8")
            break
        await asyncio.sleep(1)
    return {"image_url": image_url}
