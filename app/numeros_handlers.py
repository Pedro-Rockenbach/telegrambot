# app/numeros_handlers.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .keyboard import criar_menu_ferramentas

def menu_emergencia():
    """Cria botões que discam diretamente"""
    kb = InlineKeyboardMarkup()
    
    # Botões com url='tel:...' abrem o discador do telefone
    kb.row(
        InlineKeyboardButton("🚓 Polícia - 190", url="tel:190"),
        InlineKeyboardButton("🚑 Ambulância / SAMU - 192", url="tel:192")
    )
    kb.row(
        InlineKeyboardButton("🚒 Bombeiros - 193", url="tel:193"),
        InlineKeyboardButton("📞 Disque denúncia - 181", url="tel:181")
    )
    # CVV (Centro de Valorização da Vida)
    kb.add(InlineKeyboardButton("🩸 Centro de Valorização da Vida - 188", url="tel:188"))
    
    # Botão de voltar (usa callback para voltar ao menu do bot)
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    
    return kb

def iniciar_numeros(bot, call):
    """
    Função chamada pelo main.py.
    Recebe 'call' (o clique do botão) ou 'msg' (comando de texto).
    """
    # Verifica se veio de um botão (CallbackQuery) ou mensagem de texto (Message)
    if hasattr(call, 'message'):
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        
        # Edita a mensagem anterior para não encher a tela
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="🚨 *Números de Emergência*\n\nToque em um botão para ligar:",
            parse_mode="Markdown",
            reply_markup=menu_emergencia()
        )
    else:
        # Se foi chamado por comando de texto (/emergencia)
        bot.send_message(
            call.chat.id,
            "🚨 *Números de Emergência*\n\nToque em um botão para ligar:",
            parse_mode="Markdown",
            reply_markup=menu_emergencia()
        )
