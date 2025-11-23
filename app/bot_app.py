# app/bot_app.py
from typing import cast
from telebot import TeleBot
from .config import TOKEN, logger

from .imc_handlers import iniciar_imc
from .water_handlers import iniciar_agua
from .tmb_handlers import iniciar_tmb
from .pressao_handlers import iniciar_pressao, iniciar_afericao, enviar_info_pressao
from .riscocard_handlers import iniciar_risco
from .common_handlers import register_common_handlers, register_fallback


def create_bot():
    token = cast(str, TOKEN)
    bot = TeleBot(token)

    register_common_handlers(bot, iniciar_imc)

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

    # --- CORREÇÃO AQUI ---
    # Adicionado "calcular pressão" e "calcular pressao" na lista
    bot.register_message_handler(
        lambda m: iniciar_pressao(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in ("pressão", "pressao", "calcular pressão", "calcular pressao"),
    )

    bot.register_message_handler(
        lambda m: iniciar_afericao(bot, m),
        func=lambda m: (m.text or "").strip().lower() == "aferir pressão",
    )

    bot.register_message_handler(
        lambda m: enviar_info_pressao(bot, m),
        func=lambda m: (m.text or "").strip().lower() == "mais informações",
    )

    # --- CORREÇÃO AQUI ---
    # Adicionado .strip().lower() para normalizar o texto
    # Adicionado versões com acento e o texto exato do botão
    bot.register_message_handler(
        lambda m: iniciar_risco(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in (
            "calcular risco cardiaco",
            "calcular risco cardíaco",
            "risco cardiaco",
            "risco cardíaco",
        ),
    )

    # Agora registre o fallback por último
    register_fallback(bot, iniciar_imc)

    logger.info("Handlers registrados.")
    return bot


bot = create_bot()
