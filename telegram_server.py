import telegram, time
from telegram_token import token

t_bot = telegram.Bot(token=token)
print(t_bot.get_me())
while 1:
    updates = t_bot.get_updates()
    print(updates[0])
    time.sleep(3)
