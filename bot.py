import asyncio
from config import bot_token, chat_id
from async_bot_lib import AsyncTelegramBot
from async_pingtester_lib import AsyncPingTester

async def daily_notification(bot):
    """Отправляет уведомление о работоспособности бота раз в сутки."""
    while True:
        # Отправка уведомления
        await bot.send_message("Привет, бот работает !")
        # Ожидание 24 часа (86400 секунд)
        await asyncio.sleep(86400)

async def ip_test(bot):
    """Отправляет уведомление о недоступных хостах."""
    tester = AsyncPingTester('hosts.yml')
    unreachable_hosts = await tester.get_unreachable_hosts()
    if unreachable_hosts:
        message_bot = ', '.join([f"{item['description']}: {item['host']} нет ping" for item in unreachable_hosts])
        await bot.send_message(message_bot)

async def main():
    bot = AsyncTelegramBot(chat_id, bot_token)
    # Запуск задачи отправки уведомлений 
    asyncio.create_task(daily_notification(bot))
    while True:
        await ip_test(bot)
        # Проверка каждые 5 минут
        await asyncio.sleep(900)  # Интервал опроса хостов в секундах

if __name__ == "__main__":
    asyncio.run(main())

