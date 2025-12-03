# app/numeros_handlers.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_emergencia():
    """Cria botões que discam diretamente"""
    kb = InlineKeyboardMarkup()
    
    # Botões com url='tel:...' abrem o telefone
    kb.row(
        InlineKeyboardButton("🚓 Polícia (190)", url="tel:190"),
        InlineKeyboardButton("🚑 SAMU (192)", url="tel:192")
    )
    kb.row(
        InlineKeyboardButton("🚒 Bombeiros (193)", url="tel:193"),
        InlineKeyboardButton("📞 Denúncia (181)", url="tel:181")
    )
    # CVV (Centro de Valorização da Vida)
    kb.add(InlineKeyboardButton("🎗️ CVV - Apoio Emocional (188)", url="tel:188"))
    
    # Botão de voltar (usa callback, pois é navegação interna)
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    
    return kb

def iniciar_numeros(bot, msg):
    # Pega o chat_id corretamente (seja mensagem ou callback)
    chat_id = msg.message.chat.id if hasattr(msg, 'message') else msg.chat.id
    
    bot.send_message(
        chat_id,
        "🚨 *Números de Emergência*\n\n"
        "Toque em um botão abaixo para abrir o discador do seu telefone:",
        parse_mode="Markdown",
        reply_markup=menu_emergencia()
    )
