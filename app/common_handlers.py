
# app/common_handlers.py
from .keyboard import criar_menu_inicial, texto_cancelado, checar_cancelamento
from .config import logger

BOAS_VINDAS = (
    "Eu sou o *Hermes Bot* 🤖🩺\n"
    "Seu assistente pessoal de saúde.\n\n"
    "👇 *Como posso ajudar hoje?*"
)

MSG_QUEM_SOMOS = (
    "🤖 *Quem Somos*\n\n"
    "O Hermes Bot é um projeto desenvolvido para auxiliar no monitoramento simples de saúde.\n"
    "Nossa missão é fornecer cálculos rápidos e educativos.\n\n"
    "Desenvolvido por: [Seu Nome/Equipe]"
)

MSG_AVISOS = (
    "⚠️*Sobre o uso de dados*\n Este bot não armazena nem compartilha qualquer dado pessoal informado durante a conversa. "
    "Todas as informações são processadas apenas temporariamente para fornecer o cálculo solicitado, em conformidade com os princípios da LGPD(Lei Geral de Proteção de Dados Pessoais) . \n\n"
    "Para mais informações, fale conosco em: pedro.rockenbach@unioeste.br"
)

MSG_SAIDA = (
    "😴 *Bot em espera*\n\n"
    "Estarei por aqui aguardando. Caso queira fazer uma nova consulta, "
    "basta enviar qualquer mensagem ou digitar /menu."
)


def register_common_handlers(bot):
    """
    Registra os comandos básicos: /start, /menu e /sair.
    Não precisa mais receber função de IMC.
    """
    def start_handler(msg):
        try:
            nome = msg.from_user.first_name or "Visitante"
            mensagem = f"👋 Olá, *{nome}*! \n\n{BOAS_VINDAS}"
            
            bot.send_message(
                msg.chat.id,
                mensagem,
                reply_markup=criar_menu_inicial(),
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.exception("Erro no start: %s", e)

    def sair_handler(msg):
        bot.clear_step_handler_by_chat_id(msg.chat.id)
        bot.send_message(msg.chat.id, MSG_SAIDA, parse_mode="Markdown")

    bot.register_message_handler(start_handler, commands=["start", "menu"])
    bot.register_message_handler(sair_handler, commands=["sair"])


def register_fallback(bot):
    """
    Se o usuário digitar algo que o bot não entende, apenas mostra o menu.
    """
    def fallback(msg):
        # Se for comando de cancelar, limpa estado
        if checar_cancelamento(msg.text):
            bot.clear_step_handler_by_chat_id(msg.chat.id)
            bot.send_message(msg.chat.id, texto_cancelado(), reply_markup=criar_menu_inicial())
        else:
            # Mensagem genérica para qualquer outro texto
            bot.send_message(
                msg.chat.id,
                "🤔 Não entendi o que você digitou.\n\n👇 *Por favor, use os botões abaixo:*",
                reply_markup=criar_menu_inicial(),
                parse_mode="Markdown"
            )
            
    bot.register_message_handler(fallback, content_types=["text"])
