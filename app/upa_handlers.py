from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .keyboard import criar_menu_ferramentas, checar_cancelamento, menu_conclusao

# Banco de dados simples das UPAs (Exemplo: Cascavel-PR)
# Você pode pegar as coordenadas exatas no Google Maps (clicando com botão direito > números)
UPAS_DB = {
    "veneza": {
        "nome": "UPA Veneza",
        "endereco": "R. Café Filho, 1460 - Jardim Veneza",
        "lat": -24.982415, 
        "lon": -53.463289
    },
    "tancredo": {
        "nome": "UPA Tancredo Neves",
        "endereco": "Av. Tancredo Neves, 1453 - Centro",
        "lat": -24.965421,
        "lon": -53.490102
    },
    "brasilia": {
        "nome": "UPA Brasília",
        "endereco": "R. Europa, 1115 - Brasília",
        "lat": -24.936550, 
        "lon": -53.447810
    }
}

def menu_upas():
    """Gera os botões com os nomes das UPAs"""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🏥 Veneza", callback_data="upa_veneza"),
        InlineKeyboardButton("🏥 Tancredo", callback_data="upa_tancredo")
    )
    kb.add(InlineKeyboardButton("🏥 Brasília", callback_data="upa_brasilia"))
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    return kb

def iniciar_upas(bot, msg):
    chat_id = msg.message.chat.id if hasattr(msg, 'message') else msg.chat.id
    bot.send_message(
        chat_id,
        "🚑 *Localizar UPA*\n"
        "Selecione a unidade mais próxima para ver o mapa:",
        parse_mode="Markdown",
        reply_markup=menu_upas()
    )

def enviar_mapa_upa(bot, call):
    chat_id = call.message.chat.id
    data = call.data  # ex: upa_veneza
    chave = data.split("_")[1] # pega 'veneza'
    
    upa = UPAS_DB.get(chave)
    
    if upa:
        bot.send_chat_action(chat_id, 'find_location')
        
        # O método send_venue envia o "Mapinha Integrado"
        bot.send_venue(
            chat_id,
            latitude=upa["lat"],
            longitude=upa["lon"],
            title=upa["nome"],
            address=upa["endereco"]
        )
        
        # Pergunta o que fazer depois
        bot.send_message(
            chat_id, 
            "👆 Clique no mapa acima para abrir no GPS.",
            reply_markup=menu_conclusao()
        )
