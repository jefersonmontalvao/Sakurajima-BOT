import re
import datetime

# Code Command Handlers here. It can be functions or classes,
# but needs to have two required params, "updater" and "context".


class StartHandler:
    """
    Start bot command.
    """
    def __init__(self, updater, context):
        first_name = updater.effective_chat.first_name
        last_name = updater.effective_chat.last_name
        context.bot.send_message(chat_id=updater.effective_chat.id, text="Bem vindo %s, você agora é meu senpai." %
                                                                         first_name)


class NotifyHandler:
    instance_id = []

    def __init__(self, updater, context):
        """Get params from command line and save it ib repository
        using a JSON file. """
        # Define few important variables.
        # Updater and Context objects from telegram.
        self.__updater = updater
        self.__context = context

        # Check the subcommand and execute respective function.
        self.__get_subcommand()

    __slots__ = ('__updater', '__context')

    def __get_subcommand(self):
        self.notify_set()
        pass

    def notify_set(self):
        # Args from telegram command line.
        args = ' '.join([arg for arg in self.__context.args[1:]])

        # Necessary extract this from args.
        text = None
        created_at = None
        finish_at = None
        timer = None

        # Args filtering.
        text_pattern = re.compile("^(\"|').*('|\")")
        query = text_pattern.search(args).group(0)
        args = args.replace(query, '').strip()
        args = args.split(',')
        args[0] = query

        # Setting args.
        text = args[0][1:-1]
        created_at = datetime.datetime.now()
        finish_at = created_at + datetime.timedelta(hours=int(args[1]))
        timer = int(args[2])

        # Moving the args to a dict.
        data = {
            'text': text,
            'created_at': created_at.isoformat(),
            'finish_at': finish_at.isoformat(),
            'timer': timer
        }

    def notify_start(self):
        pass

    def notify_stop(self):
        pass
