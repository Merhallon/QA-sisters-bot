import telebot
import config
import dbworker

from telebot import types

bot = telebot.TeleBot(config.token)
first_info_text = "Привет! Мы рады приветствовать всех тестировщиц и им сочувствующих в нашем уютном и " \
                  "полезном комьюнити. Чтобы всем в нем было комфортно, мы стараемся избежать набегов ботов и троллей. " \
                  "Поэтому мы проводим небольшую пре-модерацию: хотим убедиться что вы живой человек. " \
                  "QA Sisters - это женское комьюнити, поэтому мы приглашаем только девушек. " \
                  "Разбор заявок может проходить до недели."


@bot.message_handler(commands=["start"])
@bot.inline_handler(lambda query: len(query.query) > 0)
def cmd_start(message):
    """
    Начало диалога при первом вызове /start
    """
    bot.send_message(message.chat.id, "Важно! Информация, которую вы укажете в этой форме, останется только "
                                      "между нами: мы не будем хранить эти данные и использовать их в любых интересах, "
                                      "кроме пре-модерации")
    bot.send_message(message.chat.id, f"{first_info_text}")
    bot.send_message(message.chat.id,
                     "Обращаем внимание, что мы не приемлем токсичности, грубости и оскорблений "
                     "в нашем пространстве, и придерживаемся Code of Conduct")
    bot.send_message(message.chat.id,
                     "Ознакомся с https://github.com/papers-we-love/berlin/blob/master/code-of-conduct.md")
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(
        text="Нажми меня, если согласна", callback_data="Согласна с принципами")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Если вы прочитали вышеозвученные принципы нашего комьюнити, "
                                      "пожалуйста подтвердите ваше согласие", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Меняем кнопку согласия на сообщении
    """
    if call.message:
        if call.data == "Согласна с принципами":
            bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично, спасибо!")
            bot.send_message(call.message.chat.id,
                             "Пожалуйста, укажите свою должность (если работаете) или род занятий")
            dbworker.set_state(call.message.chat.id, config.States.S_ENTER_AGE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_JOB.value)
def user_entering_name(message):
    """
    Спрашиваем ник в телеграме
    """
    bot.send_message(message.chat.id, "Оставьте здесь свой ник в телеграме, по которому вас можно найти "
                                      "(например, @example_name). "
                                      "Если ника нет, пожалуйста, создайте его в настройках учетной записи в телеграме.")
    dbworker.set_state(message.chat.id, config.States.S_NIK.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_NIK.value)
def user_entering_age(message):
    """
    Спрашиваем о соц сетях
    """
    bot.send_message(
        message.chat.id, "Здесь можно оставить ссылку на свою страницу в любой соцсети, что значительно ускорит "
                         "процесс и поможет нам убедиться, что вы не бот. Информация о ваших соцсетях останется "
                         "только между нами, мы не будем использовать эти данные в других интересах, "
                         "помимо пре-модерации.")
    dbworker.set_state(message.chat.id, config.States.S_NET.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_NET.value)
def user_sending_photo(message):
    """
    Спрашиваем откуда о нас узнали
    """
    bot.send_message(message.chat.id,
                     "Здесь можно написать, откуда вы о нас узнали")
    dbworker.set_state(message.chat.id, config.States.S_WHERE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_WHERE.value)
def user_sending_photo(message):
    """
    Спрашиваем откуда о нас узнали
    """
    bot.send_message(message.chat.id,
                     "Спасибо, за заполнение формы. Если всё хорошо, то с тобой скоро свяжется наша модераторка")


if __name__ == "__main__":
    bot.infinity_polling()
