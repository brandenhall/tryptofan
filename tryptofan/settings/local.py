from .base import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s.%(msecs).03d %(levelname)s [%(module)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/tryptofan.log',
            'maxBytes': 1000000,
            'backupCount': 4,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'root': {
        'handlers': ['logfile', 'console', ],
        'propagate': True,
        'level': 'WARNING',
    },
    'loggers': {
        'tryptofan': {
            'handlers': ['logfile', 'console', ],
            'propagate': False,
            'level': 'INFO',
        },
    },
}
