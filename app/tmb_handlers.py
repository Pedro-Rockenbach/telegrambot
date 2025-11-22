# app/tmb_handlers.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .keyboard import criar_menu_principal, checar_cancelamento, texto_cancelado
from typing import Any


def iniciar_tmb(bot: Any, msg):
    sent = bot.send_message(
        msg.chat.id,
        "Vamos calcular sua TMB.\nQual seu sexo? (Homem / Mulher)\nOu digite 'Sair'.",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        .add(KeyboardButton("Homem"))
        .add(KeyboardButton("Mulher"))
        .add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent, pegar_sexo_tmb, bot)


def pegar_sexo_tmb(message, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    sexo = (message.text or "").strip().lower()
    if not sexo or (not sexo.startswith("h") and not sexo.startswith("m")):
        sent = bot.send_message(
            message.chat.id,
            "Digite apenas 'Homem' ou 'Mulher'. Ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_sexo_tmb, bot)

    sexo_norm = "h" if sexo.startswith("h") else "m"
    sent = bot.send_message(message.chat.id, "Digite seu peso em kg (ex: 70.5).")
    bot.register_next_step_handler(sent, pegar_peso_tmb, bot, sexo_norm)


def pegar_peso_tmb(message, bot, sexo):
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
            "Peso inválido. Tente novamente (ex: 70.5) ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_peso_tmb, bot, sexo)

    sent = bot.send_message(message.chat.id, "Digite sua altura em cm (ex: 175).")
    bot.register_next_step_handler(sent, pegar_altura_tmb, bot, sexo, peso)


def pegar_altura_tmb(message, bot, sexo, peso):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").replace(",", ".").strip()
    try:
        altura = float(txt)
        if altura <= 0:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Altura inválida. Tente novamente (ex: 175) ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_altura_tmb, bot, sexo, peso)

    sent = bot.send_message(message.chat.id, "Digite sua idade (ex: 25) : ")
    bot.register_next_step_handler(sent, calcular_tmb_final, bot, sexo, peso, altura)


def calcular_tmb_final(message, bot, sexo, peso, altura):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip()
    try:
        idade = int(txt)
        if idade <= 0 or idade > 130:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Idade inválida. Tente novamente (ex: 30) ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(
            sent, calcular_tmb_final, bot, sexo, peso, altura
        )

    if sexo == "h":
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
        sexo_text = "Homem"
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
        sexo_text = "Mulher"

    texto = (
        f"Resultado da TMB:\n\n"
        f"Sexo: {sexo_text}\n"
        f"Peso: {peso:.1f} kg\n"
        f"Altura: {altura:.0f} cm\n"
        f"Idade: {idade} anos\n\n"
        f"➡️ TMB estimada: *{tmb:.2f} kcal/dia*\n\n"
        "Volte ao menu para mais opções."
    )

    bot.send_message(
        message.chat.id,
        texto,
        parse_mode="Markdown",
        reply_markup=criar_menu_principal(False),
    )
