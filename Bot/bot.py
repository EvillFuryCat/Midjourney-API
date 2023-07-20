import os
import asyncio
from discord import Client, Intents, Message


BOT_TOKEN = "MTEyODk3MTg4NjUwNDcxODM0Nw.GjdeFa.HiRVLZ-Ay_u6zI9nlQvUKdslfSl7ennSdby4Uw"
API_URL_IMAGE = os.getenv("API_URL_IMAGE")


class BotClient(Client):
    def __init__(self):
        super().__init__(intents=Intents.all())
        self.image_url = None
        self.image_event = asyncio.Event()

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message: Message, prompt: str):
        # Не реагируем на сообщения от нас самих
        if message.author == self.user:
            return

        # Проверяем, разместил ли кто-нибудь изображение в канале
        if prompt in message.content:
            if message.attachments:
                for attachment in message.attachments:
                    image_url = attachment.url
                    if attachment.url.lower().endswith(("png", "jpg", "jpeg")):
                        self.image_url = attachment.url
                        self.image_event.set()
                        return


async def get_image_url(bot: BotClient, prompt: str):
    await bot.wait_until_ready()
    await bot.image_event.wait()
    return bot.image_url


# client = BotClient()
# client.run(BOT_TOKEN)

