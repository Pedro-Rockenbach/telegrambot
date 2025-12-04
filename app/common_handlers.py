
# app/common_handlers.py
from .keyboard import criar_menu_inicial, texto_cancelado, checar_cancelamento
from .config import logger

BOAS_VINDAS = (
    "Eu sou o *Hermes Bot* 🤖🩺\n"
    "Seu assistente pessoal de saúde.\n\n"
    "Fui projetado para avaliar de forma geral sua saúde "
    "por meio de cálculos simples e informativos.\n"
    "👇 *Escolha uma opção abaixo para começar*"
)

MSG_QUEM_SOMOS = (
    "📚 *Quem Somos – PEEL Saúde e Extensão*\n"
    "Somos a PEEL Saúde e Extensão, uma equipe formada por estudantes"
    "universitários que encontrou na programação uma forma de contribuir"
    " com a comunidade. Nosso grupo é composto por Pedro Paulo, Eduardo Santana, "
    "Enrick Nunes e Luiz Alexandre, e atuamos no desenvolvimento completo do projeto"
    " — desde a análise de medidas e cálculos, até a interface, o funcionamento interno e a experiência final do usuário. "
    "\nCriamos este chatbot com o propósito de facilitar o acesso a informações básicas de saúde, como"
    " cálculos de pressão arterial, IMC, hidratação e outros dados simples que muitas pessoas precisam no dia a dia."
    " Nosso objetivo é tornar esse acesso claro, rápido e acessível, tanto para jovens acostumados à tecnologia quanto para idosos ou usuários com menos familiaridade com ferramentas digitais."
    "\nAcreditamos que, ao tornar essas informações mais acessíveis, podemos ajudar a reduzir a superlotação em unidades de saúde, permitindo que atendimentos simples sejam orientados de forma rápida e prática pelo chatbot."
)

MSG_SOBRE_HERMES = (
    "🤖 *Sobre o HERMES*\n"
    "O HERMES é um chatbot voltado para consultas simples, oferecendo cálculos, orientações básicas e acesso "
    "rápido a informações estatísticas relacionadas à saúde. Sua interface foi desenvolvida para ser confortável e "
    "intuitiva, oferecendo uma experiência direta, segura e fácil de usar."
    "\nEntre suas funções, o Hermes permite realizar cálculos automáticos, consultar unidades de saúde próximas e até acionar serviços de atendimento por discagem automática."
    "Nosso foco é promover orientação inicial, mas sempre de maneira responsável:\n"
    "o Hermes não substitui avaliação profissional, e recomendamos que qualquer dúvida mais séria ou necessidade de confirmação médica seja direcionada a um especialista em saúde."

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
