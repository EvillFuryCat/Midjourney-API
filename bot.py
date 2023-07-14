from discord import Client, Intents, Message, Attachment, User

import aiohttp

BOT_TOKEN = "MTEyODk3MTg4NjUwNDcxODM0Nw.GjdeFa.HiRVLZ-Ay_u6zI9nlQvUKdslfSl7ennSdby4Uw"


class MyClient(Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: Message):
        # Не реагируем на сообщения от нас самих
        if message.author == self.user:
            return

        # Проверяем, разместил ли кто-нибудь изображение в канале
        if message.attachments:
            for attachment in message.attachments:
                if attachment.url.lower().endswith(("png", "jpg", "jpeg")):
                    # Верни URL изображения
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                # Сохранить изображение (можно выбрать нужный путь)
                                with open(f"images/{attachment.filename}", "wb") as f:
                                    f.write(await resp.read())


client = MyClient(intents=Intents.all())
client.run(BOT_TOKEN)
