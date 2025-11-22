# app/bot_app.py
from typing import cast
from telebot import TeleBot
from .config import TOKEN, logger

# import handlers modules (they define functions we call below)
from .imc_handlers import iniciar_imc
from .water_handlers import iniciar_agua
from .tmb_handlers import iniciar_tmb
from .common_handlers import register_common_handlers


def create_bot():
    token = cast(str, TOKEN)
    bot = TeleBot(token)

    # Register common handlers (start/menu/sair/fallback) - pass iniciar_imc for backward compatibility
    register_common_handlers(bot, iniciar_imc)

    # Register other menu handlers explicitly and consistently
    bot.register_message_handler(
        lambda m: iniciar_imc(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular imc", "1"),
    )
    bot.register_message_handler(
        lambda m: iniciar_agua(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in ("calcular água", "calcular agua", "água", "agua"),
    )
    bot.register_message_handler(
        lambda m: iniciar_tmb(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular tmb", "tmb"),
    )

    logger.info("Handlers registrados.")
    return bot


bot = create_bot()
