import asyncio
import discord

from discord.ext import commands
from discord_webhook import DiscordWebhook

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests


#id_app = 1128971886504718347
CHANEL_ID = 285724843557781505
#key_app = "7eeb1290304c0110dd14ee2a7dfbfaedff17167121c0233b9fd05034222f50d5"
#BOT_TOKEN = "MTEyODk3MTg4NjUwNDcxODM0Nw.GjdeFa.HiRVLZ-Ay_u6zI9nlQvUKdslfSl7ennSdby4Uw"
#WEBHOOK_URL = "https://discord.com/api/webhooks/1129016574569881651/kwqipLXU7YpcOtVNqh1cCwwsau0YEEbn2-v09m7EOlTnRXWXUZwq5O1eJQKvvXD64ZS3"
CLIENT_TOKEN = "Mjg1MDgwMDM4NTUzMTU3NjMy.Ghtosg.EivjT7-k4jQswD4fzR3P1gQotLv12g8uhisaLE"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


app = FastAPI()


@app.post("/send-message")
async def send_message_route(message: str):
    headers = {
        'Authorization': f'{CLIENT_TOKEN}',
        'Content-Type': 'application/json'
    }

    data = {
        'content': f"/imagine : {message}"
    }

    url = f'https://discord.com/api/v9/channels/{CHANEL_ID}/messages'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return {"message": "Message sent successfully"}
    else:
        return {"message": "Failed to send message"}