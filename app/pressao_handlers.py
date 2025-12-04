# calcula a pressao
from .keyboard import (
    criar_menu_ferramentas, 
    checar_cancelamento, 
    texto_cancelado, 
    menu_pressao_inline, 
    menu_cancelar,
    menu_conclusao
)

def classificar_pressao(sistolica: int, diastolica: int) -> str:
    if sistolica < 90 or diastolica < 60:
        return "Pressão BAIXA (Hipotensão)"
    if 90 <= sistolica <= 119 and 60 <= diastolica <= 79:
        return "Pressão NORMAL"
    if 120 <= sistolica <= 139 or 80 <= diastolica <= 89:
        return "Pressão LIMÍTROFE (Pré-hipertensão)"
    if sistolica >= 140 or diastolica >= 90:
        return "Pressão ALTA (Hipertensão)"

    return "Indeterminada"

INFO_PRESSAO = (
    "📚 *Informações sobre Pressão Arterial*\n\n"
    "Pressão arterial é a força que o sangue exerce contra as paredes "
    "das artérias enquanto é bombeado pelo coração para circular pelo corpo.\n\n"
    "Valores de referência (OMS):\n"
    "🟢 Normal: < 120/80\n"
    "🟡 Limítrofe: 120-139 / 80-89\n"
    "🔴 Alta: ≥ 140/90\n\n"
    "⚠️ _Este bot não substitui um médico._"
)


def iniciar_pressao(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, 'message') else msg.chat.id
    bot.send_message(
        chat_id,
        "🩺 *Menu Pressão Arterial*\n\nO que você deseja fazer?",
        parse_mode="Markdown",
        reply_markup=menu_pressao_inline(),
    )


def iniciar_afericao_manual(bot, chat_id):
    sent = bot.send_message(
        chat_id, 
        "Digite sua pressão no formato *120/80*:", 
        parse_mode="Markdown",
        reply_markup=menu_cancelar()
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
            "📋 *Resultado da Pressão*\n\n"
            f"Sistólica: {sistolica}\n"
            f"Diastólica: {diastolica}\n\n"
            f"➡️ *Classificação*: {resultado}\n\n"
            "⚠️ Consulte um profissional se houver sintomas."
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
            "⚠️ Formato inválido! Envie no formato *120/80*.",
            parse_mode="Markdown",
            reply_markup=menu_cancelar()
        )
        bot.register_next_step_handler(sent, processar_pressao, bot)
