import logging

from sakurajima.conf import LOG_CONFIG

__all__ = ['get_logger']

# Define a basic configurations of logging. This is imported from conf.settings.py file.
LEVELS = {'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
FORMAT = LOG_CONFIG['FORMAT']

if (LEVEL := LOG_CONFIG['LEVEL'].upper()) in LEVELS:
    # Set the log format and settings
    logging.basicConfig(format=FORMAT, level=getattr(logging, LEVEL))

    # Using a file as logger.
    # logging.basicConfig(filename='debug.log', format=FORMAT, level=getattr(logging, LEVEL))
else:
    raise ValueError('LOG_CONFIG value "%s" is invalid.' % LOG_CONFIG.get('LEVEL'))


# Simplified way to get logger.
def get_logger(name='default'):
    """Return the logger with name value automatically or editable by name param."""
    name = locals().get('__name__') if name == 'default' else name
    return logging.getLogger(name)
