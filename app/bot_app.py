from typing import cast
from telebot import TeleBot
from .config import TOKEN

from .imc_handlers import iniciar_imc
from .water_handlers import iniciar_agua
from .tmb_handlers import iniciar_tmb
from .pressao_handlers import iniciar_pressao, iniciar_afericao_manual
from .riscocard_handlers import iniciar_risco
from .common_handlers import register_common_handlers, register_fallback


def create_bot():
    token = cast(str, TOKEN)
    bot = TeleBot(token)

    register_common_handlers(bot)

    bot.register_message_handler(
        lambda m: iniciar_imc(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular imc", "1"),
    )

    bot.register_message_handler(
        lambda m: iniciar_agua(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in ("calcular água", "agua", "água"),
    )

    bot.register_message_handler(
        lambda m: iniciar_tmb(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("calcular tmb", "tmb"),
    )

    # PRESSÃO: Atualizado para chamar iniciar_pressao (que abre o menu inline)
    bot.register_message_handler(
        lambda m: iniciar_pressao(bot, m),
        func=lambda m: (m.text or "").strip().lower() in ("pressão", "pressao"),
    )

    # Atalho direto para aferir: adaptado para usar iniciar_afericao_manual
    bot.register_message_handler(
        lambda m: iniciar_afericao_manual(bot, m.chat.id),
        func=lambda m: (m.text or "").strip().lower() == "aferir pressão",
    )

    bot.register_message_handler(
        lambda m: iniciar_risco(bot, m),
        func=lambda m: (m.text or "").strip().lower()
        in ("risco cardiaco", "risco cardíaco"),
    )

    # 3. Fallback (Se não entender o texto)
    register_fallback(bot)

    return bot


bot = create_bot()
