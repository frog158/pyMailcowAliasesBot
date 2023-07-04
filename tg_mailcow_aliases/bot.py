import os
import telebot
import logging
from tg_mailcow_aliases.api import add_alias
from tg_mailcow_aliases.sqlite import is_user_exist, get_user

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "error")
USER_ID = os.getenv("USER_ID", "error")

logging.info(f"USER_ID = {USER_ID}")

bot = telebot.TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    user_id = message.from_user.id
    if not is_user_exist(user_id):
        bot.reply_to(message, "403 Forbidden")
        return
    (_, name, domain, goto) = get_user(user_id)
    logging.info(f"{name} {domain} {goto}")
    bot.reply_to(message, f"Hi {name}, aliases for {domain} is goto {goto}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Получает строку и создает алиас.
    Пример ответа сервера
            [
            {
                    "log": [
                    "mailbox",
                    "add",
                    "alias",
                    {
                            "active": "1",
                            "address": "alias@domain.tld",
                            "goto": "destination@domain.tld"
                    },
                    null
                    ],
                    "msg": [
                    "alias_added",
                    "alias@domain.tld"
                    ],
                    "type": "success"
            }
            ]
    """
    # полученый текст наша левая часть
    alias = message.text
    # айди пользователя
    user_id = str(message.from_user.id)
    # Если пользователь не разрешен то отлуп
    if user_id != USER_ID:
        bot.reply_to(message, "403 Forbidden")
        return
    logging.info(f"User - {user_id}, URL - {alias}")
    # создаем алиас. По умолчани можно передать только левую часть алиаса
    # там есть дефолтные значения
    (status_code, result) = add_alias(alias)
    # STATUS_CODE ответ сервера. Если не 200 значит что то не так в принципе
    # не связи или сервер не отвечает
    logging.info(f"STATUS_CODE = {status_code}")
    # result это результат. Выше есть пример ответа
    logging.info(f"Server response = {result}")
    # Если не 200 то какая то ошибка надо смотреть в логи
    if status_code != 200:
        bot.reply_to(message, "General error")
        return
    result_type = result[0]["type"]
    # Если создали то отвечаем пользователю что алиас создан
    if result_type == "success":
        alias = result[0]["log"][3]["address"]
        goto = result[0]["log"][3]["goto"]
        bot.reply_to(message, f"✅ Success!\nAddress {alias} goto {goto}")
    else:
        # Если не смогли то сообщаем об ошибке
        # и выводим то что нам сервер прислал
        msg = f"{result[0]['msg'][0]} {result[0]['msg'][1]}"
        bot.reply_to(message, f"🆘 Failed!\nTYPE = {result_type}\n{msg}")


def start_bot():
    bot.polling()
