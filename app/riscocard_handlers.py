
from typing import Dict
from .keyboard import (
    criar_menu_ferramentas,  # Substituiu criar_menu_principal
    texto_cancelado,
    checar_cancelamento,
    menu_sim_nao,
    menu_sexo,
    menu_cancelar,
    menu_conclusao,  # Novo menu de fim
)

RISK_INTRO = (
    "Vamos fazer uma estimativa rápida.\n\nPrimeiro, digite sua *idade*:"
)

RISK_DISCLAIMER = (
    "⚠️ *Aviso*: Este cálculo é apenas educativo e baseado em estatísticas gerais. "
    "Não substitui exames clínicos."
)

# Cache temporário
RISCO_CACHE = {}


def iniciar_risco(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, "message") else msg.chat.id
    RISCO_CACHE[chat_id] = {}
    riscocard = (
        f"🫀 *Risco Cardiáco* \n\nO cálculo de risco cardíaco é uma ferramenta usada para estimar a probabilidade de uma pessoa ter um evento cardiovascular, como infarto ou AVC, nos próximos 10 anos."
    ) 
    bot.send_message(
        chat_id, riscocard, parse_mode="Markdown"
    )
    sent = bot.send_message(
        chat_id, RISK_INTRO, parse_mode="Markdown", reply_markup=menu_cancelar()
    )
    bot.register_next_step_handler(sent, pegar_idade, bot)


def pegar_idade(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return

    try:
        idade = int(message.text)
        if not (10 < idade < 120):
            raise ValueError
    except:
        sent = bot.send_message(
            chat_id, "⚠️ Idade inválida. Digite novamente:", reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, pegar_idade, bot)

    if chat_id in RISCO_CACHE:
        RISCO_CACHE[chat_id]["idade"] = idade

    # Próximo passo: Sexo (Botões)
    bot.send_message(
        chat_id, "Qual seu sexo biológico?", reply_markup=menu_sexo("risco")
    )


def callback_risco_sexo(bot, call):
    chat_id = call.message.chat.id
    if chat_id not in RISCO_CACHE:
        RISCO_CACHE[chat_id] = {}

    RISCO_CACHE[chat_id]["sexo"] = "M" if "sexo_m" in call.data else "F"

    bot.send_message(
        chat_id,
        "🚬 Você fuma atualmente?",
        reply_markup=menu_sim_nao("risco", "fumante"),
    )


def callback_risco_fumante(bot, call):
    chat_id = call.message.chat.id
    is_sim = "_s" in call.data
    if chat_id in RISCO_CACHE:
        RISCO_CACHE[chat_id]["fumante"] = is_sim

    bot.send_message(
        chat_id,
        "🍬 Possui diagnóstico de diabetes?",
        reply_markup=menu_sim_nao("risco", "diabetes"),
    )


def callback_risco_diabetes(bot, call):
    chat_id = call.message.chat.id
    is_sim = "_s" in call.data
    if chat_id in RISCO_CACHE:
        RISCO_CACHE[chat_id]["diabetes"] = is_sim
    
    sent = bot.send_message(
        chat_id,
        "🩺 Digite sua pressão sistólica (o valor maior, ex: *120*):",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_sbp, bot)


def pegar_sbp(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return

    try:
        sbp = int(float(message.text.replace(",", ".")))
    except:
        sent = bot.send_message(
            chat_id,
            "⚠️ Valor inválido. Digite apenas o número (ex: 120):",
            reply_markup=menu_cancelar(),
        )
        return bot.register_next_step_handler(sent, pegar_sbp, bot)

    if chat_id in RISCO_CACHE:
        RISCO_CACHE[chat_id]["sbp"] = sbp

    sent = bot.send_message(
        chat_id,
        "🍔 Digite seu Colesterol Total (mg/dL) (ex: *190*):",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent, pegar_chol, bot)


def pegar_chol(message, bot):
    chat_id = message.chat.id
    if checar_cancelamento(message.text):
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )
        return

    try:
        chol = float(message.text.replace(",", "."))
    except:
        sent = bot.send_message(
            chat_id,
            "⚠️ Inválido. Digite o colesterol (ex: 190):",
            reply_markup=menu_cancelar(),
        )
        return bot.register_next_step_handler(sent, pegar_chol, bot)

    if chat_id in RISCO_CACHE:
        RISCO_CACHE[chat_id]["chol"] = chol
        dados = RISCO_CACHE[chat_id]
    else:
        dados = {}

    resultado_texto = _calcular_risco(dados)

    # Formatação final bonita
    mensagem_final = f"{resultado_texto}\n\n{RISK_DISCLAIMER}\n"

    bot.send_message(
        chat_id, mensagem_final, parse_mode="Markdown", reply_markup=menu_conclusao()
    )

    # Limpa memória
    if chat_id in RISCO_CACHE:
        del RISCO_CACHE[chat_id]


def _calcular_risco(data: Dict) -> str:
    # Lógica simplificada de pontos (WHO/ISH adaptada para exemplo)
    idade = data.get("idade", 30)
    sexo = data.get("sexo", "M")
    fumante = data.get("fumante", False)
    diabetes = data.get("diabetes", False)
    sbp = data.get("sbp", 120)

    points = 0

    if idade >= 40:
        points += 1
    if idade >= 50:
        points += 1
    if idade >= 60:
        points += 1

    if sexo == "M":
        points += 1
    if fumante:
        points += 2
    if diabetes:
        points += 2
    if sbp >= 140:
        points += 1
    if sbp >= 160:
        points += 1

    # Classificação visual
    if points <= 2:
        nivel = "🟢 BAIXO (<10%)"
    elif 3 <= points <= 5:
        nivel = "🟡 MODERADO (10-20%)"
    else:
        nivel = "🔴 ALTO (>20%)"

    return (
        f"❤️ *ESTIMATIVA DE RISCO*\n\n"
        f"👤 *Perfil:* {sexo}, {idade} anos\n"
        f"🚬 *Fumante:* {'Sim' if fumante else 'Não'}\n"
        f"🍬 *Diabetes:* {'Sim' if diabetes else 'Não'}\n"
        f"🩺 *Pressão:* {sbp} mmHg\n\n"
        f"📊 *Resultado:* {nivel}"
    )
