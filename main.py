import os
import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Lê token da variável de ambiente
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "A variável de ambiente TELEGRAM_TOKEN não está definida. "
        "Defina-a localmente ou no painel do Railway antes de rodar."
    )

bot = telebot.TeleBot(TOKEN)


# Cria um teclado visual
def criar_menu_principal(one_time=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    kb.add(KeyboardButton("Calcular IMC"))
    kb.add(KeyboardButton("Sair"))
    return kb


def texto_cancelado():
    return "Operação cancelada. Volte ao menu principal quando quiser."


def checar_cancelamento(text):
    if text is None:
        return False
    t = text.strip().lower()
    return t in ("sair", "/sair", "cancel", "/cancel", "cancelar", "/cancelar")


def classificar_imc(imc):
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


@bot.message_handler(commands=["start", "menu"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "Bem-vindo! Escolha uma opção:",
        reply_markup=criar_menu_principal(one_time=False),
    )


@bot.message_handler(
    func=lambda m: m.text is not None
    and m.text.strip().lower() in ["calcular imc", "1"]
)
def iniciar_imc(msg):
    # pede peso
    sent = bot.send_message(
        msg.chat.id,
        "Ok — vamos calcular seu IMC.\nDigite seu peso em kg (ex: 70 ou 70.5). Para cancelar, digite 'Sair'.",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent, pegar_peso)


@bot.message_handler(
    func=lambda m: m.text is not None and m.text.strip().lower() in ["sair", "/sair"]
)
def sair_menu(msg):
    bot.send_message(
        msg.chat.id,
        texto_cancelado(),
        reply_markup=criar_menu_principal(one_time=False),
    )


def pegar_peso(msg):
    if checar_cancelamento(msg.text):
        bot.send_message(
            msg.chat.id,
            texto_cancelado(),
            reply_markup=criar_menu_principal(one_time=False),
        )
        return

    txt = msg.text.replace(",", ".").strip()
    try:
        peso = float(txt)
        if peso <= 0:
            raise ValueError
    except:
        sent = bot.send_message(
            msg.chat.id,
            "Peso inválido. Digite o peso em kg usando apenas números (ex: 70 ou 70.5). Ou digite 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_peso)

    # pede altura
    sent2 = bot.send_message(
        msg.chat.id,
        "Agora digite sua altura em metros (ex: 1.75). Para cancelar, digite 'Sair'.",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(KeyboardButton("Sair")),
    )
    bot.register_next_step_handler(sent2, pegar_altura, peso)


def pegar_altura(msg, peso):
    if checar_cancelamento(msg.text):
        bot.send_message(
            msg.chat.id,
            texto_cancelado(),
            reply_markup=criar_menu_principal(one_time=False),
        )
        return

    txt = msg.text.replace(",", ".").strip()
    try:
        altura = float(txt)
        if altura <= 0:
            raise ValueError
    except:
        sent = bot.send_message(
            msg.chat.id,
            "Altura inválida. Digite algo como 1.70 (use ponto ou vírgula). Ou digite 'Sair' para cancelar.",
        )
        return bot.register_next_step_handler(sent, pegar_altura, peso)

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
        msg.chat.id, resposta, reply_markup=criar_menu_principal(one_time=False)
    )


# Captura qualquer outro texto (quando quiser manter o menu funcionando)
@bot.message_handler(content_types=["text"])
def qualquer_texto(msg):
    txt = msg.text.strip().lower()
    if txt in ("calcular imc", "1"):
        # já existe handler específico, mas mantemos fallback
        iniciar_imc(msg)
    elif checar_cancelamento(txt):
        bot.send_message(
            msg.chat.id,
            texto_cancelado(),
            reply_markup=criar_menu_principal(one_time=False),
        )
    else:
        bot.send_message(
            msg.chat.id,
            "Escolha uma opção do menu:",
            reply_markup=criar_menu_principal(one_time=False),
        )


if __name__ == "__main__":
    logger.info("Bot rodando (polling)...")
    # Mantém polling contínuo; Railway irá manter o processo vivo
    bot.polling(non_stop=True)

