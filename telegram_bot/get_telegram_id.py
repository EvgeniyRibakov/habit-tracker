import telegram
import asyncio
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def get_updates():
    try:
        bot = telegram.Bot(token='8166531317:AAGosFPZVf7jGrvMGRxTSKcEF0JT0axdG9c')
        # Увеличиваем таймаут до 30 секунд
        updates = await bot.get_updates(timeout=30)
        if not updates:
            logging.info("Нет новых обновлений. Убедитесь, что вы отправили сообщение боту (например, /start).")
            return
        for update in updates:
            chat_id = update.message.chat_id
            logging.info(f"Chat ID: {chat_id}")
            print(f"Chat ID: {chat_id}")
    except telegram.error.TimedOut as e:
        logging.error(f"Таймаут при получении обновлений: {e}")
        print("Произошёл таймаут. Попробуйте снова или проверьте подключение к интернету.")
    except telegram.error.TelegramError as e:
        logging.error(f"Ошибка Telegram API: {e}")
        print(f"Произошла ошибка Telegram: {e}")


if __name__ == "__main__":
    asyncio.run(get_updates())
