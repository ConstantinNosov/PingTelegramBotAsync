import aiohttp

class AsyncTelegramBot:
    def __init__(self, chat_id, bot_token):
        self.chat_id = chat_id
        self.bot_token = bot_token
        self.session = aiohttp.ClientSession()

    async def send_message(self, message):
        """Асинхронно отправляет сообщение боту."""
        async with self.session.get(
            url=f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            params={
                'chat_id': self.chat_id,
                'text': message
            }
        ) as response:
            return await response.json()

    async def close(self):
        await self.session.close()

        

