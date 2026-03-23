import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from tg_mailcow_aliases.api import add_alias
from tg_mailcow_aliases.sqlite import is_user_exist, get_user

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "error")
PROXY_URL = os.getenv("PROXY_URL", None)
PROXY_USERNAME = os.getenv("PROXY_USERNAME", None)
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", None)

# Словарь с переводом ошибок от mailcow
ERROR_MESSAGES = {
    "is_alias_or_mailbox": "Алиас или ящик уже существует",
    "alias_invalid": "Неверный формат алиаса",
    "access_denied": "Нет доступа",
    "invalid_request": "Неверный запрос",
    "general_error": "Ошибка сервера mailcow",
}

dp = Dispatcher()


def create_bot():
    if PROXY_URL:
        if PROXY_USERNAME and PROXY_PASSWORD:
            proxy = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}"
        else:
            proxy = f"http://{PROXY_URL}"
        session = AiohttpSession(proxy=proxy)
        logging.info(f"Bot initialized with proxy: {PROXY_URL}")
        return Bot(token=TG_BOT_TOKEN, session=session)
    logging.info("Bot initialized without proxy")
    return Bot(token=TG_BOT_TOKEN)


@dp.message(Command("start", "help"))
async def start(message):
    user_id = message.from_user.id
    if not is_user_exist(user_id):
        await message.reply("403 Forbidden")
        return
    (_, name, domain, goto) = get_user(user_id)
    logging.info(f"{user_id} {name} {domain} {goto}")
    await message.reply(f"Hi {name}, aliases for {domain} is goto {goto}")


@dp.message(F.text)
async def handle_message(message):
    alias = message.text
    user_id = str(message.from_user.id)
    if not is_user_exist(user_id):
        await message.reply("403 Forbidden")
        return
    (_, name, domain, goto) = get_user(user_id)
    logging.info(f"{user_id}, {name}  {alias}@{domain} goto {goto}")
    (status_code, result) = await asyncio.to_thread(add_alias, alias, goto, domain)
    logging.info(f"STATUS_CODE = {status_code}")
    logging.info(f"Server response = {result}")
    if status_code != 200:
        await message.reply("General error")
        return
    result_type = result[0]["type"]
    if result_type == "success":
        alias = result[0]["log"][3]["address"]
        goto = result[0]["log"][3]["goto"]
        await message.reply(
            f"✅ Success!\nAddress `{alias}` goto {goto}",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        error_code = result[0]["msg"][0]
        error_target = result[0]["msg"][1]
        error_text = ERROR_MESSAGES.get(error_code, error_code)
        await message.reply(
            f"❌ Ошибка!\n`{error_target}`\n{error_text}",
            parse_mode=ParseMode.MARKDOWN,
        )


async def start_polling():
    bot = create_bot()
    await dp.start_polling(bot)
