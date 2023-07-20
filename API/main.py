import asyncio
import json
import aiohttp
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from API.bot import BotClient, BOT_TOKEN
from celery import Celery

class Item(BaseModel):
    message: str

CHANNEL_ID = os.getenv("CHANNEL_ID")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")


app = FastAPI()
celery = Celery("tasks", broker="redis://127.0.0.1:6379/0", backend="redis://localhost:6379/0")

celery.conf.update(
     broker_connection_retry_on_startup=True,
     task_serializer="json",
     result_serializer="json",
     accept_content=["json"],
     timezone="Europe/Moscow",
)

@celery.task(bind=True)
def send_message_to_discord(self, message: str):
    try:
        async def send_message():
            headers = {
                "Authorization": "MTEyNzg4MjI5NjcyNTM1MjQ0OA.G4VeKE.RY2t7qleC67G3mY_n9tGGvmMk3BoW1HrXqHeLo",
                "Content-Type": "application/json",
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
                            "value": "",
                        }
                    ],
                },
            }

            url = "https://discord.com/api/v9/interactions"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    print("#####", response)
                    if response.status == 204:
                        return True
                    else:
                        return False

        asyncio.run(send_message())
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", e)

     
@app.post("/send-message")
async def send_message_route(prompt: Item, request: Request):
    message = prompt.message
    task = send_message_to_discord.delay(message)  # Start the Celery task to send message to Discord
    task_result = task.wait()
    print(task_result)
    bot = BotClient()
    await bot.start(BOT_TOKEN)
    await bot.wait_until_ready()
    await bot.image_event.wait()
    image_url = bot.image_url
    await bot.close()
    return {"image_url": image_url}
# @app.post("/send-message")
# async def send_message_route(prompt: Item, request: Request):
#     headers = {
#         "Authorization": f"{CLIENT_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "type": 2,
#         "application_id": "936929561302675456",
#         "guild_id": f"{CHANNEL_ID}",
#         "channel_id": f"{CHANNEL_ID}",
#         "session_id": "effacc7b-e32c-4002-8f61-d4b471fe22c7",
#         "data": {
#             "version": "1118961510123847772",
#             "id": "938956540159881230",
#             "name": "imagine",
#             "type": 1,
#             "options": [
#                 {
#                     "type": 3,
#                     "name": "prompt",
#                     "description": "What is the question?",
#                     "required": True,
#                     "value": f"{prompt.message}",
#                 }
#             ],
#         },
#     }

#     url = "https://discord.com/api/v9/interactions"
    
#     async with session.post(url, headers=headers, json=data) as response:
#         if response.status == 204:
#             message = await response.json()
#             message_id = message["id"]
#             channel_id = message["channel_id"]
#             await bot.wait_until_ready()
#             bot.image_event.clear()
#             bot.image_url = None
#             await bot.wait_for("message", channel=channel_id, message_id=message_id, prompt=prompt.message)
#             if bot.image_url:
#                 return {"image_url": bot.image_url}
#             else:
#                 return {"message": "No image URL found"}
#         else:
#             return {"message": "Failed to send message to Discord API"}

