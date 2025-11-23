from typing import Dict
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from .keyboard import criar_menu_principal, texto_cancelado, checar_cancelamento
from .config import logger

RISK_INTRO = (
    "Vamos estimar um risco cardiovascular aproximado.\n\n"
    "Vou te fazer algumas perguntas rápidas (idade, sexo, tabagismo, diabetes, "
    "pressão sistólica e colesterol total). Responda usando números ou 'Sim'/'Não'.\n\n"
    "Para cancelar a qualquer momento digite 'Sair'."
)

RISK_DISCLAIMER = (
    "⚠️ *Aviso*: este é um cálculo aproximado e educativo. Não substitui avaliação médica. "
    "Se tiver dúvidas ou sintomas, procure um profissional de saúde."
)

# ---------- Fluxo: iniciar -> idade -> sexo -> tabagismo -> diabetes -> sbp -> colesterol -> resultado


def sim_ou_nao():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Sim"))
    kb.add(KeyboardButton("Não"))
    kb.add(KeyboardButton("Sair"))
    return kb


def iniciar_risco(bot, msg):
    """Inicia o fluxo de cálculo de risco cardíaco."""
    logger.info(
        "Iniciando fluxo de risco para chat_id=%s", getattr(msg.chat, "id", None)
    )
    sent = bot.send_message(msg.chat.id, RISK_INTRO)
    # pergunta idade no próximo passo
    bot.register_next_step_handler(sent, pegar_idade, {}, bot)


def pegar_idade(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip()
    try:
        idade = int(txt)
        if idade <= 0 or idade > 120:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Idade inválida. Digite sua idade em anos (ex: 45). Ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_idade, data, bot)

    data["idade"] = idade
    sent2 = bot.send_message(
        message.chat.id,
        "Qual seu sexo? ",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        .add(KeyboardButton("Masculino"))
        .add(KeyboardButton("Feminio"))
        .add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent2, pegar_sexo, data, bot)


def pegar_sexo(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip().lower()
    if txt in ("m", "masculino", "homem"):
        data["sexo"] = "M"
    elif txt in ("f", "feminino", "mulher"):
        data["sexo"] = "F"
    else:
        sent = bot.send_message(
            message.chat.id,
            "Resposta inválida. Digite 'M' (masculino) ou 'F' (feminino). Ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_sexo, data, bot)

    sent2 = bot.send_message(
        message.chat.id,
        "Você é fumante atualmente? (Sim/Não)",
        reply_markup=sim_ou_nao(),
    )
    bot.register_next_step_handler(sent2, pegar_tabagismo, data, bot)


def pegar_tabagismo(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip().lower()
    data["fumante"] = txt in ("sim", "s", "yes", "y")
    sent2 = bot.send_message(
        message.chat.id,
        "Tem diagnóstico de diabetes? (Sim/Não)",
        reply_markup=sim_ou_nao(),
    )
    bot.register_next_step_handler(sent2, pegar_diabetes, data, bot)


def pegar_diabetes(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip().lower()
    data["diabetes"] = txt in ("sim", "s", "yes", "y")
    sent2 = bot.send_message(
        message.chat.id,
        "Digite sua pressão arterial sistólica (ex: 120)",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent2, pegar_sbp, data, bot)


def pegar_sbp(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip().replace(",", ".")
    try:
        sbp = int(float(txt))
        if sbp <= 50 or sbp >= 300:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Pressão inválida. Digite a pressão sistólica em mmHg (ex: 120). Ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_sbp, data, bot)

    data["sbp"] = sbp
    sent2 = bot.send_message(
        message.chat.id,
        "Digite o colesterol total em mg/dL (ex: 190).",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent2, pegar_chol, data, bot)


def pegar_chol(message, data: Dict, bot):
    if checar_cancelamento(message.text):
        bot.send_message(
            message.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )
        return

    txt = (message.text or "").strip().replace(",", ".")
    try:
        chol = float(txt)
        if chol <= 50 or chol >= 1000:
            raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "Colesterol inválido. Digite o colesterol total em mg/dL (ex: 190). Ou 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_chol, data, bot)

    data["chol"] = chol
    resultado = _calcular_risco(data)
    bot.send_message(
        message.chat.id, resultado + "\n\n" + RISK_DISCLAIMER, parse_mode="Markdown"
    )
    bot.send_message(
        message.chat.id,
        "Volte ao menu principal:",
        reply_markup=criar_menu_principal(False),
    )


def _calcular_risco(data: Dict) -> str:
    """
    Estimativa heurística simplificada — educational only.
    Pontos baseados em faixas de idade, sexo, tabagismo, diabetes, PAS, colesterol.
    Mapeamento final converte pontos para classificação percentual aproximada.
    """
    idade = data.get("idade", 0)
    sexo = data.get("sexo", "M")
    fumante = data.get("fumante", False)
    diabetes = data.get("diabetes", False)
    sbp = data.get("sbp", 0)
    chol = data.get("chol", 0.0)

    points = 0

    # idade
    if idade < 40:
        points += 0
    elif 40 <= idade < 50:
        points += 5
    elif 50 <= idade < 60:
        points += 8
    elif 60 <= idade < 70:
        points += 10
    else:
        points += 12

    # sexo
    if sexo == "M":
        points += 3

    # tabagismo
    if fumante:
        points += 4

    # diabetes
    if diabetes:
        points += 5

    # pressão sistólica
    if sbp < 120:
        points += 0
    elif 120 <= sbp < 140:
        points += 2
    elif 140 <= sbp < 160:
        points += 4
    else:
        points += 6

    # colesterol total (mg/dL)
    if chol < 200:
        points += 0
    elif 200 <= chol < 240:
        points += 2
    elif 240 <= chol < 280:
        points += 4
    else:
        points += 6

    # mapear pontos para risco aproximado (apenas indicativo)
    if points <= 4:
        risk_pct = "<5%"
        category = "Baixo risco"
    elif 5 <= points <= 9:
        risk_pct = "≈5-10%"
        category = "Risco moderado"
    elif 10 <= points <= 14:
        risk_pct = "≈10-20%"
        category = "Risco alto"
    else:
        risk_pct = ">20%"
        category = "Risco muito alto"

    resumo = (
        f"*Estimativa de risco cardíaco (heurística simplificada)*\n\n"
        f"Categoria: *{category}*\n"
        f"Estimativa: *{risk_pct}* (apenas indicativa)\n\n"
        f"_Pontos totais_: {points}\n\n"
        "Fatores considerados: idade, sexo, tabagismo, diabetes, pressão sistólica e colesterol total.\n\n"
        "Fonte: Organização Mundial da Saúde (OMS) (Lancet, 2019)."
    )
    return resumo
