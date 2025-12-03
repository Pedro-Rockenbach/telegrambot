
# app/pressao_handlers.py
from .keyboard import (
    criar_menu_ferramentas,
    checar_cancelamento,
    texto_cancelado,
    menu_pressao_inline,
    menu_cancelar,
    menu_conclusao,
)


def classificar_pressao(sistolica: int, diastolica: int) -> str:
    if sistolica < 90 or diastolica < 60:
        return "Pressão BAIXA"
    if 90 <= sistolica <= 119 and 60 <= diastolica <= 79:
        return "Pressão NORMAL"
    if 120 <= sistolica <= 139 or 80 <= diastolica <= 89:
        return "Pré-hipertensão"
    if sistolica >= 140 or diastolica >= 90:
        return "ALTA (Hipertensão)"
    return "Indeterminada"


INFO_PRESSAO = (
    "📚 *Informações sobre Pressão Arterial*\n\n"
    "Valores de referência (OMS):\n"
    "🟢 Normal: < 120/80\n"
    "🟡 Limítrofe: 120-139 / 80-89\n"
    "🔴 Alta: ≥ 140/90"
)


def iniciar_pressao(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, "message") else msg.chat.id
    bot.send_message(
        chat_id,
        "🩺 *Menu Pressão Arterial*",
        parse_mode="Markdown",
        reply_markup=menu_pressao_inline(),
    )


def iniciar_afericao_manual(bot, chat_id):
    sent = bot.send_message(
        chat_id,
        "Digite sua pressão (*ex: 120/80*):",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, processar_pressao, bot)


def processar_pressao(message, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return

    try:
        valor = message.text.replace(" ", "").replace(".", "").replace(",", "")
        if "/" not in valor:
            raise ValueError
        sistolica, diastolica = map(int, valor.split("/"))
        resultado = classificar_pressao(sistolica, diastolica)

        resposta = (
            "📋 *RESULTADO PRESSÃO*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Medida: *{sistolica} / {diastolica}*\n"
            f"➡️ Classificação: *{resultado}*\n\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(
            message.chat.id,
            resposta,
            parse_mode="Markdown",
            reply_markup=menu_conclusao(),
        )

    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "⚠️ Formato inválido! Tente *120/80*:",
            parse_mode="Markdown",
            reply_markup=menu_cancelar(),
        )
        bot.register_next_step_handler(sent, processar_pressao, bot)
