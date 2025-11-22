# app/bot_app.py
from typing import cast
from telebot import TeleBot
from .config import TOKEN, logger
from .imc_handlers import iniciar_imc
from .common_handlers import register_common_handlers


def create_bot():
    token = cast(str, TOKEN)
    bot = TeleBot(token)
    register_common_handlers(bot, iniciar_imc)
    logger.info("Handlers registrados.")
    return bot


bot = create_bot()
