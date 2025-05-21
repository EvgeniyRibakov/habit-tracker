import telegram
import asyncio


async def send_test_message():
    bot = telegram.Bot(token='8166531317:AAGosFPZVf7jGrvMGRxTSKcEF0JT0axdG9c')
    try:
        # Замените на ваш предполагаемый chat_id (если вы его знаете) или используйте после получения
        await bot.send_message(chat_id='963382703', text="Тестовое сообщение от бота")
        print("Сообщение отправлено успешно!")
    except telegram.error.TelegramError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(send_test_message())
