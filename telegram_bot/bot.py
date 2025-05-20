import telegram
from django.conf import settings


async def send_telegram_message(telegram_id, message):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=telegram_id, text=message)
    except telegram.error.TelegramError as e:
        print(f"Failed to send Telegram message: {e}")
