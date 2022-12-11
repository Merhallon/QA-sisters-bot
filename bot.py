import logging
import rules
import os
import exceptions

from aiogram import Bot, Dispatcher, executor, types
from middlewares import AccessMiddleware


API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(bot, CHAT_ID, ADMIN_CHAT_ID))


def set_key(key: str = None):

    def decorator(func):
        setattr(func, 'key', key)
        return func

    return decorator


@dp.message_handler(commands="start")
async def start_massage(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня, чтобы получить правила", callback_data="get"))
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня, чтобы добавить правила", callback_data="add"))
    await message.answer("Привет! Это qaSistersFirstBot \n"
                         "Нажмите на кнопку, чтобы выбрать действие", reply_markup=keyboard)


@dp.callback_query_handler(text="get")
async def with_puree(call: types.CallbackQuery):
    """Присылает правила"""
    rules_from_bd = rules.get_all_rules_from_bd()
    if not rules_from_bd:
        await call.message.answer("Правил ещё нет")
        return
    list_of_rules = [
            f"{rul.id}) {rul.rules_text}"
            for rul in rules_from_bd]
    answer_message = "Ознакомься с правилами:\n\n " + "\n\n ".join(list_of_rules)
    await call.message.answer(answer_message)


@dp.callback_query_handler(text="add")
@set_key('admin')
async def with_puree(callback: types.CallbackQuery):
    """Присылает ответ админу"""
    answer_message = "Напишите новое правило"
    await callback.message.answer(answer_message)


@dp.message_handler()
@set_key('admin')
async def add_rule(message: types.Message):
    """Добавляет новое правило"""
    try:
        rule = rules.add_rules(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлено новое правило - {rule.rules_text}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
