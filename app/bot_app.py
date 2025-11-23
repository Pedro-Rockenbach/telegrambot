# app/bot_app.py
from typing import cast
from telebot import TeleBot
from .config import TOKEN, logger

from .imc_handlers import iniciar_imc
from .water_handlers import iniciar_agua
from .tmb_handlers import iniciar_tmb
from .pressure_handlers import iniciar_pressao, iniciar_afericao, enviar_info_pressao
from .common_handlers import register_common_handlers, register_fallback


def create_bot():
    token = cast(str, TOKEN)
    bot = TeleBot(token)

    # Register start and sair (common), but NOT fallback yet
    register_common_handlers(bot, iniciar_imc)

    # Register specific handlers FIRST (priority)
    bot.register_message_handler(
        lambda m: iniciar_imc(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular imc", "1"),
    )
    bot.register_message_handler(
        lambda m: iniciar_agua(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in ("calcular água", "calcular agua", "água", "agua", "calcular agua"),
    )
    bot.register_message_handler(
        lambda m: iniciar_tmb(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular tmb", "tmb"),
    )
    bot.register_message_handler(
        lambda m: iniciar_pressao(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("pressão", "pressao"),
    )

    bot.register_message_handler(
        lambda m: iniciar_afericao(bot, m),
        func=lambda m: (m.text or "").strip().lower() == "aferir pressão",
    )

    bot.register_message_handler(
        lambda m: enviar_info_pressao(bot, m),
        func=lambda m: (m.text or "").strip().lower() == "mais informações",
    )

    # Agora registre o fallback por último (garante que ele só será acionado se nenhuma das regras acima combinar)
    register_fallback(bot, iniciar_imc)

    logger.info("Handlers registrados.")
    return bot


bot = create_bot()
