import aiohttp
import asyncio
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

async def get_updates(offset: int = None) -> Dict[str, Any]:
    """Получает обновления от Telegram API"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            print(f"Ошибка при получении обновлений: {e}")
            return {}

async def send_message(chat_id: int, text: str) -> None:
    """Отправляет сообщение пользователю"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                await response.json()
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def main():
    offset = None
    while True:
        updates = await get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                message = update.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')

                if text == '/start':
                    await send_message(chat_id, "Привет! Я бот для знакомства с Telegram API.")
                
                offset = update['update_id'] + 1

if __name__ == "__main__":
    asyncio.run(main())
