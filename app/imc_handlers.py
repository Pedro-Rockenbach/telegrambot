# app/i
# app/imc_handlers.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .keyboard import checar_cancelamento, criar_menu_principal, texto_cancelado
from .config import logger


def classificar_imc(imc: float) -> str:
    if imc < 18.5:
        return "Abaixo do peso"
    if 18.5 <= imc < 25:
        return "Peso normal"
    if 25 <= imc < 30:
        return "Sobrepeso"
    if 30 <= imc < 35:
        return "Obesidade grau I"
    if 35 <= imc < 40:
        return "Obesidade grau II"
    return "Obesidade grau III (mórbida)"


def _sair_markup():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton("Sair")
    )


# assinatura: iniciar_imc(bot, message)
def iniciar_imc(bot, msg):
    logger.info("Iniciando fluxo IMC para chat_id=%s", getattr(msg.chat, "id", None))
    sent = bot.send_message(
        msg.chat.id,
        "Ok — vamos calcular seu IMC.\nDigite seu peso em kg (ex: 70 ou 70.5). Para cancelar, digite 'Sair'.",
        reply_markup=_sair_markup(),
    )
    bot.register_next_step_handler(sent, pegar_peso, bot)


def pegar_peso(message, bot):
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
            "Peso inválido. Digite o peso em kg usando apenas números (ex: 70 ou 70.5). Ou digite 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_peso, bot)

    sent2 = bot.send_message(
        message.chat.id,
        "Agora digite sua altura em metros (ex: 1.75). Para cancelar, digite 'Sair'.",
        reply_markup=_sair_markup(),
    )
    bot.register_next_step_handler(sent2, pegar_altura, bot, peso)


def pegar_altura(message, bot, peso):
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
            "Altura inválida. Digite algo como 1.70 (use ponto ou vírgula). Ou digite 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_altura, bot, peso)

    imc = peso / (altura**2)
    categoria = classificar_imc(imc)

    resposta = (
        f"Resultado:\n\n"
        f"Peso: {peso:.2f} kg\n"
        f"Altura: {altura:.2f} m\n"
        f"IMC: {imc:.2f}\n"
        f"Classificação: {categoria}\n\n"
        "Legenda (WHO):\n"
        " - Abaixo do peso: < 18.5\n"
        " - Normal: 18.5 – 24.9\n"
        " - Sobrepeso: 25 – 29.9\n"
        " - Obesidade I: 30 – 34.9\n"
        " - Obesidade II: 35 – 39.9\n"
        " - Obesidade III: ≥ 40\n\n"
        "Volte ao menu principal ou calcule novamente."
    )

    bot.send_message(
        message.chat.id, resposta, reply_markup=criar_menu_principal(False)
    )
