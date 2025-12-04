# main.py
from app.bot_app import bot
from app.keyboard import criar_menu_inicial, criar_menu_ferramentas, texto_cancelado
from app.common_handlers import MSG_QUEM_SOMOS, MSG_AVISOS, MSG_SAIDA, MSG_SOBRE_HERMES

from app.imc_handlers import iniciar_imc, imc_calcular, iniciar_calculo_imc_manual
from app.tmb_handlers import iniciar_tmb, callback_tmb_sexo
from app.water_handlers import iniciar_agua
from app.riscocard_handlers import (
    iniciar_risco,
    callback_risco_sexo,
    callback_risco_fumante,
    callback_risco_diabetes,
)
from app.pressao_handlers import iniciar_pressao, iniciar_afericao_manual, INFO_PRESSAO
from app.upa_handlers import iniciar_upas, enviar_mapa_upa
from app.numeros_handlers import iniciar_numeros

@bot.callback_query_handler(func=lambda call: True)
def callback_router(call):
    data = call.data
    chat_id = call.message.chat.id


    if data == "voltar_inicio":
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"🏠 *Menu Principal*\nEscolha uma opção:",
            parse_mode="Markdown",
            reply_markup=criar_menu_inicial(),
        )

    elif data == "abrir_ferramentas":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="🛠 *Área de Avaliação*\nQual cálculo deseja realizar?",
            parse_mode="Markdown",
            reply_markup=criar_menu_ferramentas(),
        )

    elif data == "quem_somos":
        bot.send_message(
            chat_id,
            MSG_QUEM_SOMOS,
            parse_mode="Markdown",
            reply_markup=criar_menu_inicial(),
        )
    elif data == "sobre_hermes":
        bot.send_message(
            chat_id, MSG_SOBRE_HERMES, parse_mode="Markdown",
            reply_markup=criar_menu_inicial(),
        )

    elif data == "avisos":
        bot.send_message(
            chat_id,
            MSG_AVISOS,
            parse_mode="Markdown",
            reply_markup=criar_menu_inicial(),
        )

    elif data == "sair_final":
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.send_message(chat_id, MSG_SAIDA, parse_mode="Markdown")

    elif data == "cancelar_voltar_ferramentas":
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.send_message(
            chat_id, texto_cancelado(), reply_markup=criar_menu_ferramentas()
        )

    # --- FERRAMENTAS ---
    elif data == "imc":
        iniciar_imc(bot, call)
    elif data == "tmb":
        iniciar_tmb(bot, call)
    elif data == "agua":
        iniciar_agua(bot, call)
    elif data == "risco":
        iniciar_risco(bot, call)
    elif data == "pressao":
        iniciar_pressao(bot, call)
    elif data == "upas":
        iniciar_upas(bot, call)
    elif data == "numeros": # <--- NOVO HANDLER
        iniciar_numeros(bot, call)
    # --- PRESSÃO ---
    elif data == "pressao_aferir":
        iniciar_afericao_manual(bot, chat_id)
    elif data == "pressao_info":
        bot.send_message(chat_id, INFO_PRESSAO, parse_mode="Markdown")
        iniciar_pressao(bot, call)

    #menu secundario do imc
    elif data == "imc_calcular":
        iniciar_calculo_imc_manual(bot, call)
    # --- FLUXOS INTERNOS (TMB/RISCO) ---
    elif data.startswith("tmb_sexo"):
        callback_tmb_sexo(bot, call)
    elif data.startswith("risco_sexo"):
        callback_risco_sexo(bot, call)
    elif data.startswith("risco_fumante"):
        callback_risco_fumante(bot, call)
    elif data.startswith("risco_diabetes"):
        callback_risco_diabetes(bot, call)
    elif data.startswith("upa_"): # Captura upa_veneza, upa_tancredo, etc.
        enviar_mapa_upa(bot, call)

    bot.answer_callback_query(call.id)


if __name__ == "__main__":
    print("Bot rodando com Nova Navegação...")
    bot.infinity_polling()
