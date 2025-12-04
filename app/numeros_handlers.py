# app/numeros_handlers.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_emergencia():
    """Cria apenas o botão de voltar, já que os números estarão no texto"""
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    return kb

def iniciar_numeros(bot, call):
    """Mostra os números como texto clicável"""
    
    # Texto formatado para facilitar o clique no celular
    texto_emergencia = (
        "🚨 *NÚMEROS DE EMERGÊNCIA*\n"
        "🚓 Polícia - 190\n\n"
        "🚑 Ambulância / SAMU - 192\n\n"
        "🚒 Bombeiros - 193\n\n"
        "📞 Disque Denúncia - 181\n\n"
        "🩸 Centro de Valorização da Vida - 188\n\n",
        "⚠️ _Em caso de risco iminente, não dependa apenas do bot._"
    )

    if hasattr(call, 'message'):
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=texto_emergencia,
            parse_mode="Markdown",
            reply_markup=menu_emergencia()
        )
    else:
        bot.send_message(
            call.chat.id,
            texto_emergencia,
            parse_mode="Markdown",
            reply_markup=menu_emergencia()
        )
