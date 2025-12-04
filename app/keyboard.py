
# app/keyboard.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def criar_menu_inicial():
    kb = InlineKeyboardMarkup()
    # Botão de Ação principal
    kb.add(
        InlineKeyboardButton("🚀 Ir para Avaliação", callback_data="abrir_ferramentas")
    )
    # Botões informativos
    kb.row(
        InlineKeyboardButton("🎒 Quem Somos", callback_data="quem_somos"),
        InlineKeyboardButton("🤖 Sobre o Hermes", callback_data="sobre_hermes"),
    )

    kb.add(
        InlineKeyboardButton("⚠ Avisos importantes", callback_data="avisos")
    )
    return kb

def criar_menu_ferramentas():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("📊 IMC", callback_data="imc"),
        InlineKeyboardButton("💧 Água", callback_data="agua"),
    )
    kb.row(
        InlineKeyboardButton("🔥 TMB", callback_data="tmb"),
        InlineKeyboardButton("🩺 Pressão", callback_data="pressao"),
    )
    kb.row(
        InlineKeyboardButton("❤️ Risco Cardíaco", callback_data="risco"),
        InlineKeyboardButton("🚨 Emergência", callback_data="abrir_emergencia_menu"),
    # Botão para voltar ao início
    kb.add(InlineKeyboardButton("🔙 Voltar ao Início", callback_data="voltar_inicio"))
    return kb

def menu_emergencia_secundario():
    """Novo Submenu específico para Emergências"""
    kb = InlineKeyboardMarkup()
    
    kb.add(InlineKeyboardButton("🚑 Mapa de UPAs (GPS)", callback_data="upas"))
    kb.add(InlineKeyboardButton("📞 Números Úteis", callback_data="numeros"))
    
    # Voltar para o menu de ferramentas (nível anterior)
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    
    return kb

def menu_conclusao():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🏠 Menu Principal", callback_data="voltar_inicio"),
        InlineKeyboardButton("👋 Sair", callback_data="sair_final"),
    )
    return kb


# --- Outros Menus Auxiliares (Mantidos) ---


def menu_cancelar():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "❌ Cancelar Operação", callback_data="cancelar_voltar_ferramentas"
        )
    )
    return kb


def menu_sexo(prefixo):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("👨 Homem", callback_data=f"{prefixo}_sexo_m"),
        InlineKeyboardButton("👩 Mulher", callback_data=f"{prefixo}_sexo_f"),
    )
    kb.add(
        InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_voltar_ferramentas")
    )
    return kb


def menu_sim_nao(prefixo, etapa):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("✅ Sim", callback_data=f"{prefixo}_{etapa}_s"),
        InlineKeyboardButton("❌ Não", callback_data=f"{prefixo}_{etapa}_n"),
    )
    kb.add(
        InlineKeyboardButton("↩️ Cancelar", callback_data="cancelar_voltar_ferramentas")
    )
    return kb


def menu_pressao_inline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🩺 Aferir Agora", callback_data="pressao_aferir"))
    kb.row(
        InlineKeyboardButton("ℹ️ Info", callback_data="pressao_info"),
        InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"),
    )
    return kb

def menu_imc_inline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🧮 Calcular IMC", callback_data="imc_calcular"))
    kb.add(InlineKeyboardButton("🔙 Voltar", callback_data="abrir_ferramentas"))
    return kb

def texto_cancelado():
    return "🚫 Operação cancelada."


def checar_cancelamento(text):
    if text is None:
        return False
    t = text.strip().lower()
    return t in ("sair", "/sair", "cancel", "/cancel", "cancelar", "/cancelar")
