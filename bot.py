from discord import Client, Intents, Message
import aiohttp
import requests

BOT_TOKEN = "MTEyODk3MTg4NjUwNDcxODM0Nw.GjdeFa.HiRVLZ-Ay_u6zI9nlQvUKdslfSl7ennSdby4Uw"


class MyClient(Client):
    def __init__(self, api_url):
        super().__init__(intents=Intents.all())
        self.api_url = api_url
    
    async def on_ready(self):
        print("Logged on as", self.user)


    async def on_message(self, message: Message):
        # Не реагируем на сообщения от нас самих
        if message.author == self.user:
            return

        # Проверяем, разместил ли кто-нибудь изображение в канале
        if message.attachments:
            for attachment in message.attachments:
                if attachment.url.lower().endswith(("png", "jpg", "jpeg")):
                    # Верни URL изображения
                    with open(f"{attachment.filename}.jpg", "wb") as f:
                        response = requests.get(attachment.url)
                        f.write(response.content)
                    with open(f"{attachment.filename}.jpg", "rb") as f:
                        files = {"image": f}
                        response = requests.post(self.api_url, files=files)
                    if response.status_code == 200:
                        print("Image uploaded successfully")
                    else:
                        print("Failed to upload image")
                        

client = MyClient(api_url="http://0.0.0.0:8000/image/")
client.run(BOT_TOKEN)
