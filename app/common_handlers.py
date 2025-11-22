# app/common_handlers.py
from .keyboard import criar_menu_principal, texto_cancelado, checar_cancelamento
from .config import logger

BOAS_VINDAS = (
    "Olá! Eu sou o *Hermes Bot*, seu assistente pessoal em saúde. 👋\n\n"
    "Posso te ajudar com cálculos rápidos (ex.: IMC, TMB, Água, risco cardíaco). Use o menu abaixo para começar."
)

DISCLAIMER = (
    "⚠️ *Aviso importante*: as informações fornecidas por este bot são apenas informativas "
    "e não substituem a avaliação de um profissional de saúde. Em caso de emergência, procure atendimento."
)


def register_common_handlers(bot, iniciar_imc_func):
    """
    Registra handlers universais:
    - /start e /menu: envia boas-vindas + disclaimer
    - sair: cancela o fluxo atual
    - fallback: rota de fallback que encaminha para iniciar_imc_func se texto indicar
    Note: iniciar_imc_func é passado apenas para manter compatibilidade com o menu antigo;
    mas o IMC agora tem seu próprio módulo e também será registrado explicitamente em bot_app.
    """

    def start_handler(msg):
        try:
            bot.send_message(
                msg.chat.id,
                BOAS_VINDAS,
                reply_markup=criar_menu_principal(False),
                parse_mode="Markdown",
            )
            bot.send_message(msg.chat.id, DISCLAIMER, parse_mode="Markdown")
        except Exception as e:
            logger.exception("Erro ao enviar start/disclaimer: %s", e)

    def sair_handler(msg):
        bot.send_message(
            msg.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
        )

    def fallback(msg):
        txt = (msg.text or "").strip().lower()
        # manter compatibilidade: se querem o IMC via texto, encaminha para a função passada
        if txt in ("calcular imc", "1"):
            iniciar_imc_func(bot, msg)
        elif checar_cancelamento(txt):
            bot.send_message(
                msg.chat.id, texto_cancelado(), reply_markup=criar_menu_principal(False)
            )
        else:
            bot.send_message(
                msg.chat.id,
                "Escolha uma opção do menu:",
                reply_markup=criar_menu_principal(False),
            )

    bot.register_message_handler(start_handler, commands=["start", "menu"])
    bot.register_message_handler(
        sair_handler, func=lambda m: (m.text or "").strip().lower() in ("sair", "/sair")
    )
    bot.register_message_handler(fallback, content_types=["text"])
