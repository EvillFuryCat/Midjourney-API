import discord

from discord.ext import commands


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests


# Создай модель для сообщения
class Item(BaseModel):
    message: str


CHANEL_ID = 285724843557781505
CLIENT_TOKEN = "Mjg1MDgwMDM4NTUzMTU3NjMy.Ghtosg.EivjT7-k4jQswD4fzR3P1gQotLv12g8uhisaLE"

app = FastAPI()


@app.post("/send-message")
async def send_message_route(message: str):
    headers = {
        'Authorization': f'{CLIENT_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        'content': f"/imagine prompt:{message}"
    }

    url = f'https://discord.com/api/v9/channels/{CHANEL_ID}/messages'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return {"message": "Message sent successfully"}
    else:
        return {"message": "Failed to send message"}
    
    
@app.post('/image/')
async def send_image_url(item: Item):
    return JSONResponse(status_code=200, content=item.message)