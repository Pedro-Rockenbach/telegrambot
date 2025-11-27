# main.py
from app.bot_app import bot

if __name__ == "__main__":
    bot.polling(non_stop=True)
