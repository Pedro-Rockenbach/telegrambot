# app/keyboard.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def criar_menu_principal(one_time=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    kb.add(KeyboardButton("Calcular IMC"))
    kb.add(KeyboardButton("Calcular Água"))
    kb.add(KeyboardButton("Calcular TMB"))
    kb.add(KeyboardButton("Calcular pressão"))
    kb.add(KeyboardButton("Calcular Risco Cardíaco"))
    kb.add(KeyboardButton("Sair"))
    return kb


def texto_cancelado():
    return "Operação cancelada. Volte ao menu principal quando quiser."


def checar_cancelamento(text):
    if text is None:
        return False
    t = text.strip().lower()
    return t in ("sair", "/sair", "cancel", "/cancel", "cancelar", "/cancelar")
