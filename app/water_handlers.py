
# app/water_handlers.py
from .keyboard import (
    criar_menu_ferramentas,
    checar_cancelamento,
    texto_cancelado,
    menu_cancelar,
    menu_conclusao,
)


def iniciar_agua(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, "message") else msg.chat.id
    sent = bot.send_message(
        chat_id,
        "💧 *Vamos calcular seu consumo diário de água.*\n\nDigite seu peso em *kg*:",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_peso_agua, bot)


def pegar_peso_agua(message, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return

    try:
        peso = float(message.text.replace(",", "."))
        if peso <= 0:
            raise ValueError
    except:
        sent = bot.send_message(
            message.chat.id,
            "⚠️ Peso inválido. Tente novamente:",
            reply_markup=menu_cancelar(),
        )
        return bot.register_next_step_handler(sent, pegar_peso_agua, bot)

    agua_litros = (peso * 35) / 1000.0

    texto = (
        f"💧 *Consumo diário recomendado de água*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Para seu peso de {peso:.1f} kg:\n\n"
        f"➡️ *{agua_litros:.2f} litros* por dia.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"fonte: Organização Mundial da Saúde."
    )

    bot.send_message(
        message.chat.id, texto, parse_mode="Markdown", reply_markup=menu_conclusao()
    )
