# app/imc_handlers.py
from .keyboard import (
    criar_menu_ferramentas,
    texto_cancelado,
    checar_cancelamento,
    menu_cancelar,
    menu_conclusao,
)


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


def gerar_barra_imc(imc):
    imc_limite = max(15, min(imc, 40))
    percentual = (imc_limite - 15) / (40 - 15)
    cheios = int(percentual * 10)
    return "🟩" * cheios + "⬜" * (10 - cheios)


def iniciar_imc(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, "message") else msg.chat.id
    sent = bot.send_message(
        chat_id,
        "⚖️ *Cálculo de IMC*\n\nDigite seu peso em *kg*:",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_peso, bot)


def pegar_peso(message, bot):
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
        return bot.register_next_step_handler(sent, pegar_peso, bot)

    sent = bot.send_message(
        message.chat.id,
        "📏 Agora sua altura em *metros*:",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_altura, bot, peso)


def pegar_altura(message, bot, peso):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return
    try:
        altura = float(message.text.replace(",", "."))
        if altura > 100:
            altura /= 100
        if altura <= 0:
            raise ValueError
    except:
        sent = bot.send_message(
            message.chat.id,
            "⚠️ Altura inválida. Tente novamente:",
            reply_markup=menu_cancelar(),
        )
        return bot.register_next_step_handler(sent, pegar_altura, bot, peso)

    imc = peso / (altura**2)
    categoria = classificar_imc(imc)
    barra = gerar_barra_imc(imc)

    resposta = (
        f"📊 *RESULTADO DO IMC*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 *Dados:* {peso}kg | {altura}m\n"
        f"👉 *IMC:* {imc:.2f}\n"
        f"[{barra}]\n"
        f"🏷 *Status:* {categoria}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )

    # AQUI: Usa menu_conclusao (Menu Principal / Sair)
    bot.send_message(
        message.chat.id, resposta, parse_mode="Markdown", reply_markup=menu_conclusao()
    )

