# app/water_handlers.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .keyboard import criar_menu_principal, checar_cancelamento, texto_cancelado
from typing import Any


def iniciar_agua(bot: Any, msg):
    sent = bot.send_message(
        msg.chat.id,
        "Vamos calcular seu consumo diário de água.\nDigite seu peso em kg (ex: 70.5). Ou digite 'Sair'.",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent, pegar_peso_agua, bot)


def pegar_peso_agua(message, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").replace(",", ".").strip()
    try:
        peso = float(txt)
        if peso <= 0:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Peso inválido. Digite novamente (ex: 70.5) ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_peso_agua, bot)

    # Consumo recomendado: 35 ml por kg
    agua_ml = peso * 35
    agua_litros = agua_ml / 1000.0

    texto = (
        f"Consumo diário recomendado de água:\n\n"
        f"Peso: {peso:.1f} kg\n"
        f"➡️ Você deve beber aproximadamente *{agua_litros:.2f} litros* de água por dia.\n\n"
        "Volte ao menu para mais opções."
    )

    bot.send_message(
        message.chat.id,
        texto,
        parse_mode="Markdown",
        reply_markup=criar_menu_principal(False),
    )
