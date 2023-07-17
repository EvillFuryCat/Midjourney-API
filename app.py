import json
from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import discord
import requests
import httpx
from discord.ext import commands


# Создай модель для сообщения
class Item(BaseModel):
    message: str


CHANEL_ID = 285724843557781505
CLIENT_TOKEN = "Mjg1MDgwMDM4NTUzMTU3NjMy.GiOReY.VR0aJJa-DIx87babkNrNbVA7xi4t6l52yqC5DQ"

app = FastAPI()




@app.post("/send-message")
async def send_message_route(prompt: str):
    headers = {"Authorization": f"{CLIENT_TOKEN}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    data = {
   "type":2,
   "application_id":"936929561302675456",
   "guild_id":"285724843557781505",
   "channel_id":"285724843557781505",
   "session_id":"effacc7b-e32c-4002-8f61-d4b471fe22c7",
   "data":{
      "version":"1118961510123847772",
      "id":"938956540159881230",
      "name":"imagine",
      "type": 1,
      "options":[
         {
            "type":3,
            "name":"prompt",
            "description":"What is the question?",
            "required":True,
            "value": f"{prompt}"
         }
      ]
   }
}

    url = "https://discord.com/api/v9/interactions"
    response = requests.post(url, headers=headers, json=data, )
    if response.status_code == 204:
        return {"message": "Message sent successfully"}
    else:
        return {"message": "Failed to send message"}


@app.post("/image/")
async def process_image(image: UploadFile):
    file_path = f"images/{image.filename}"
    with open(file_path, "wb") as f:
        f.write(await image.read())
    return {"message": "Image uploaded successfully"}
