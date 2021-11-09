from telegram.ext import Updater
from sakurajima.conf import TOKEN, HANDLERS
from .models_handler import ModelsHandler
from .logger import get_logger

logger = get_logger(__name__)


class Sakurajima:
    def __init__(self) -> None:
        logger.info('Bot started')
        # Define few variables containing telegram bot objects.
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Import database base_models.
        ModelsHandler()

        # Import handler base_models.
        self.load_handlers(HANDLERS)

    def load_handlers(self, handler_list) -> None:
        """Load the imported handlers from 'conf.settings.py'"""
        for handler in handler_list:
            self.dispatcher.add_handler(handler)

    def run(self) -> None:
        """Run bot method."""
        self.updater.start_polling()


def run_bot() -> None:
    """
    This functions is used to run the all bot.
    It's imported from here to "sakurajima/run.py".
    """
    # Bot class instance.
    sakurajima_bot = Sakurajima()
    sakurajima_bot.run()
