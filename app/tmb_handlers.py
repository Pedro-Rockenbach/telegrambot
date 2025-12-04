

# app/tmb_handlers.py
from .keyboard import (
    criar_menu_ferramentas,
    checar_cancelamento,
    texto_cancelado,
    menu_sexo,
    menu_cancelar,
    menu_conclusao,
)

TMB_CACHE = {}


def iniciar_tmb(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, "message") else msg.chat.id
    TMB_CACHE[chat_id] = {}
    bot.send_message(
        chat_id,
        f"🔥 *Cálculo de Taxa Metabólica Basal*\n\n"
        "A Taxa Metabólica Basal (TMB) é a quantidade mínima de calorias que seu corpo precisa para\n"
        "manter funções vitais em repouso absoluto, como respiração, circulação sanguínea e manutenção da temperatura corporal.",
        parse_mode="Markdown"
    )
    bot.send_message(
        chat_id,
        "Para começar o cálculo, selecione seu sexo biológico?\n",
        parse_mode="Markdown",
        reply_markup=menu_sexo("tmb")
    )


def callback_tmb_sexo(bot, call):
    chat_id = call.message.chat.id
    sexo = "h" if "sexo_m" in call.data else "m"
    TMB_CACHE[chat_id] = {"sexo": sexo}
    sent = bot.send_message(
        chat_id,
        "Digite seu *peso* em kg:",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_peso_tmb, bot)


def pegar_peso_tmb(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return
    try:
        peso = float(message.text.replace(",", "."))
        if chat_id in TMB_CACHE:
            TMB_CACHE[chat_id]["peso"] = peso
    except:
        sent = bot.send_message(
            chat_id, "Peso inválido. Tente novamente:", reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, pegar_peso_tmb, bot)

    sent = bot.send_message(
        chat_id,
        "Digite sua *altura* em cm (ex: 175):",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_altura_tmb, bot)


def pegar_altura_tmb(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return
    try:
        altura = float(message.text.replace(",", "."))
        if chat_id in TMB_CACHE:
            TMB_CACHE[chat_id]["altura"] = altura
    except:
        sent = bot.send_message(
            chat_id, "Altura inválida. Tente novamente:", reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, pegar_altura_tmb, bot)

    sent = bot.send_message(
        chat_id,
        "Digite sua *idade*:",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, calcular_final, bot)


def calcular_final(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return
    try:
        idade = int(message.text)
    except:
        sent = bot.send_message(
            chat_id, "Idade inválida. Tente novamente:", reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, calcular_final, bot)

    data = TMB_CACHE.get(chat_id, {})
    peso = data.get("peso", 70)
    altura = data.get("altura", 170)
    sexo = data.get("sexo", "m")

    if sexo == "h":
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
        sexo_text = "Homem"
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
        sexo_text = "Mulher"

    bot.send_message(
        chat_id,
        f"🔥 *RESULTADO TMB*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Dados: {sexo_text}, {peso}kg, {altura:.0f}cm, {idade} anos\n"
        f"➡️ Gasto Basal: *{tmb:.0f} kcal/dia*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"fonte: Equação de Harris-Benedict",
        parse_mode="Markdown"
    )

    bot.send_message(
        chat_id,
        f"⚠ *aviso*\n\n Esse é um cálculo estimado baseado em uma fórmula matemática. "
        "Para informações mais precisas, consulte um profissional da saúde.",
        parse_mode="Markdown",
        reply_markup=menu_conclusao()
    )
    if chat_id in TMB_CACHE:
        del TMB_CACHE[chat_id]
