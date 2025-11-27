from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .keyboard import criar_menu_principal, checar_cancelamento, texto_cancelado


# --- Classificação da pressão ---
def classificar_pressao(sistolica: int, diastolica: int) -> str:
    if sistolica < 90 or diastolica < 60:
        return "Pressão BAIXA"
    if 90 <= sistolica <= 119 and 60 <= diastolica <= 79:
        return "Pressão NORMAL"
    if 120 <= sistolica <= 139 or 80 <= diastolica <= 89:
        return "Pressão LIMÍTROFE (Pré-hipertensão)"
    if sistolica >= 140 or diastolica >= 90:
        return "Pressão ALTA (Hipertensão)"

    return "Não foi possível classificar."


# --- Teclado ---
def criar_menu_pressao():
    teclado = ReplyKeyboardMarkup(resize_keyboard=True)
    teclado.add(KeyboardButton("Aferir Pressão"))
    teclado.add(KeyboardButton("Mais Informações"))
    teclado.add(KeyboardButton("Voltar"))
    return teclado


# --- Mensagem de informações ---
INFO_PRESSAO = (
    " Informações sobre Pressão Arterial\n\n"
    "Valores de referência usados pelo HERMES:\n"
    "- Baixa: abaixo de 90/60\n"
    "- Normal: entre 90/60 e 119/79\n"
    "- Limítrofe: entre 120/80 e 139/89\n"
    "- Alta: 140/90 ou mais\n\n"
    "fonte: Organização Mundial da Saúde\n\n"
    " Este bot não substitui avaliação profissional."
)


# --- Handler principal ---
def iniciar_pressao(bot, msg):
    """
    Entrada principal do menu de pressão arterial.
    """
    bot.send_message(
        msg.chat.id,
        "Escolha uma opção sobre pressão arterial:",
        reply_markup=criar_menu_pressao(),
    )


def iniciar_afericao(bot, msg):
    """
    Inicia coleta da pressão: pergunta 120/80.
    """
    sent = bot.send_message(
        msg.chat.id, "Digite sua pressão no formato *120/80*:", parse_mode="Markdown"
    )
    bot.register_next_step_handler(sent, processar_pressao, bot)


def processar_pressao(message, bot):
    """
    Processa o valor 120/80 e classifica.
    """
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    try:
        valor = message.text.replace(" ", "")
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
            reply_markup=criar_menu_principal(False),
        )

    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Formato inválido! Envie no formato *120/80*.",
            parse_mode="Markdown",
        )
        bot.register_next_step_handler(sent, processar_pressao, bot)


def enviar_info_pressao(bot, msg):
    """
    Envia texto informativo sobre classificação da pressão arterial.
    """
    bot.send_message(
        msg.chat.id,
        INFO_PRESSAO,
        parse_mode="Markdown",
        reply_markup=criar_menu_pressao(),
    )
