import os
import telegram
import asyncio

async def send_telegram_alert(message):
    """Sends an alert message to a specific Telegram chat asynchronously."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("Telegram environment variables not set. Skipping notification.")
        return

    try:
        # Note: The library name is 'telegram', the class is 'Bot'.
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"Successfully sent Telegram alert to chat ID {chat_id}")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")