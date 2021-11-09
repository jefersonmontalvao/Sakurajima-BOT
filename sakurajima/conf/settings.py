from sakurajima.controller import StartHandler, NotifyHandler
from telegram.ext.commandhandler import CommandHandler

# Insert here your bot token:
TOKEN = open(r'D:\GitHub\MyProjects\telegram-bot\excluded\key.txt', 'r', encoding='utf8').read()

# Configure the logging module format here. By default it will be keep this way.
LOG_CONFIG = {
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LEVEL': 'info',
}

# Set command handler list here.
HANDLERS = [
    CommandHandler('start', StartHandler),
    CommandHandler('notify', NotifyHandler)
]

# Database settings here.
DATABASE = {
    'BACKEND': 'sakurajima.db.backends.sqlite3',
    'NAME': 'sakurajima-application'
}
