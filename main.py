# main.py
from app.bot_app import bot
from app.config import logger

if __name__ == "__main__":
    logger.info("Iniciando polling...")
    bot.polling(non_stop=True)

