# app/imc_handlers.py
from .keyboard import (
    criar_menu_ferramentas, 
    texto_cancelado, 
    checar_cancelamento, 
    menu_cancelar, 
    menu_conclusao,
    menu_imc_inline
)

from time import sleep

def classificar_imc(imc: float) -> str:
    if imc < 18.5: return "Abaixo do peso"
    if 18.5 <= imc < 25: return "Peso normal"
    if 25 <= imc < 30: return "Sobrepeso"
    if 30 <= imc < 35: return "Obesidade grau I"
    if 35 <= imc < 40: return "Obesidade grau II"
    return "Obesidade grau III (mórbida)"

def gerar_barra_imc(imc):
    # Cria uma barra visual de 10 blocos
    imc_limite = max(15, min(imc, 40)) 
    percentual = (imc_limite - 15) / (40 - 15)
    cheios = int(percentual * 10)
    return "🟩" * cheios + "⬜" * (10 - cheios)

def iniciar_imc(bot, msg):
    """Inicia o fluxo de cálculo do IMC."""
    chat_id = msg.message.chat.id if hasattr(msg, 'message') else msg.chat.id
    
    sent = bot.send_message(
        chat_id,
        "⚖️ *Índice de Massa Corporal*\n\n O IMC é um cálculo que relaciona o peso e a altura de uma pessoa, ajudando-a avaliar seu peso ideal.\n"
        "\n\n👇Para avaliar seu IMC, clique em 'Cálcular IMC' logo abaixo:\n\n",
        parse_mode="Markdown",
        reply_markup=menu_imc_inline(),
    )

def iniciar_calculo_imc_manual(bot, chat_id):
    sent = bot.send_message(
        chat_id, 
        "Passo 1:\n\nDigite seu peso em *kg* (ex: 70.5):\n", 
        parse_mode="Markdown",
        reply_markup=menu_cancelar()
    )
    bot.register_next_step_handler(sent, pegar_peso, bot)


    
def pegar_peso(message, bot):
    if checar_cancelamento(message.text):
        bot.send_message(message.chat.id, texto_cancelado(), reply_markup=criar_menu_ferramentas())
        return

    txt = (message.text or "").replace(",", ".").strip()
    try:
        peso = float(txt)
        if peso <= 0: raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "ooops!\n\n⚠️ Peso inválido.\n\nDigite apenas números (ex: 70.5):",
            reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, pegar_peso, bot)

    sent2 = bot.send_message(
        message.chat.id,
        "Passo 2:\n\n📏 Agora digite sua altura em *metros* (ex: 1.75):\n",
        parse_mode="Markdown",
        reply_markup=menu_cancelar(),
    )
    bot.register_next_step_handler(sent2, pegar_altura, bot, peso)

def pegar_altura(message, bot, peso):
    if checar_cancelamento(message.text):
        bot.send_message(message.chat.id, texto_cancelado(), reply_markup=criar_menu_ferramentas())
        return

    txt = (message.text or "").replace(",", ".").strip()
    try:
        altura = float(txt)
        if altura > 100: altura /= 100 # Corrige se digitar em cm
        if altura <= 0: raise ValueError
    except Exception:
        sent = bot.send_message(
            message.chat.id,
            "ooops!\n\n⚠️ Altura inválida. Use ponto ou vírgula (ex: 1.75):\n",
            reply_markup=menu_cancelar()
        )
        return bot.register_next_step_handler(sent, pegar_altura, bot, peso)

    imc = peso / (altura**2)
    categoria = classificar_imc(imc)
    barra = gerar_barra_imc(imc)

    resposta = (
        f"📊 *RESULTADO DO IMC*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 *Dados:* {peso}kg | {altura}m\n"
        f"👉 *IMC:* {imc:.2f}\n"
        f"[{barra}]\n"
        f"🏷 *Status:* {categoria}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" 
        f"fonte: Organização Mundial da Saúde (OMS)" 
    )
    
    bot.send_message(message.chat.id, resposta, parse_mode="Markdown")

    sleep(2)

    resposta2 = (
        f"━━━━━━━━ ⚠ atenção ━━━━━━━━━━━━\n" 
        f"Esse cálculo é apenas informativo " 
        f"e segue os critérios recomendados " 
        f"pela OMS. O resultado não substitui uma avaliação" 
        f"com um profissional da saúde.\n\n" 
    )

    bot.send_message(message.chat.id, resposta2, parse_mode="Markdown", reply_markup=menu_conclusao())
