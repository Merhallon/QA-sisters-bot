"""Аутентификация — пропускаем сообщения только от одного Telegram аккаунта"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):

    statuses = ['creator', 'administrator', 'member']

    def __init__(self, bot, chat_id: int, admin_chat_id: int):
        self.bot = bot
        self.chat_id = chat_id
        self.admin_chat_id = admin_chat_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        # здесь у нас общая проверка на большую группу
        # для того, чтобы это заработала бот должен быть админом в обоих чатах
        user_status = await self.bot.get_chat_member(chat_id=self.chat_id, user_id=message.from_user.id)
        status = str(user_status.status)
        if status not in self.statuses:
            await message.answer("Вы не можете использовать бота, так как не состоите в основной группе QA sisters")
            raise CancelHandler()

        # здесь проверка на админство для фукнций c set_key('admin')
        handler = current_handler.get()
        if handler:
            key = getattr(handler, 'key', "Такого атрибута нет")
            if key == 'admin':
                user_status_admin = await self.bot.get_chat_member(chat_id=self.admin_chat_id,
                                                                   user_id=message.from_user.id)
                admin_status = str(user_status_admin.status)
                if admin_status not in self.statuses:
                    await message.answer("Вы не можете совершить это действие, "
                                         "так как не состоите в чате админок QA sisters")
                    raise CancelHandler()

    async def on_process_callback_query(self, call: types.CallbackQuery, message: types.Message):
        # здесь проверка на админство при callback-е
        callback_text = call.data
        if callback_text == 'add':
            user_status_admin = await self.bot.get_chat_member(chat_id=self.admin_chat_id, user_id=call.from_user.id)
            admin_status = str(user_status_admin.status)
            if admin_status not in self.statuses:
                raise CancelHandler()
