from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from gimini_bot.app.states import AI
import google.generativeai as genai
from gimini_bot.config import AI_TOKEN
from gimini_bot.app.database.requests import set_user

router = Router()
genai.configure(api_key=AI_TOKEN)
model = genai.GenerativeModel('gemini-1.5-flash')


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer('*Добро пожаловать в бот с ИИ*')
    await state.clear()


@router.message(AI.answer)
async def answer(message: Message, state: FSMContext):
    await message.answer('Подождите, идет генерация запроса')


@router.message(AI.question)
@router.message(F.text)
async def ai(message: Message, state: FSMContext):
    await state.set_state(AI.answer)
    try:
        chat = (await state.get_data())['context']
        if len(chat.history) > 10:
            chat = model.start_chat(history=[])
        response = await chat.send_message_async(message.text)
        await state.update_data(context=chat)
    except:
        chat = model.start_chat(history=[])
        response = await chat.send_message_async(message.text)
        await state.update_data(context=chat)
    await message.answer(response.text)
    await state.set_state(AI.question)
