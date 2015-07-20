import logging
from logging.config import dictConfig


logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
        'handlers': {
            'default': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter':'standard',
                },
            'persistant': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'formatter':'standard',
                'filename':'logs/work.log',
                'backupCount':10,
                },


            },
        'loggers': {
            '': {
                'handlers': ['default', 'persistant'],
                'level': 'DEBUG',
                'propagate': True
                },
            'bad_things': {
                'handlers': ['default'],
                'level': 'WARN',
                'propagate': False
                },
            }
        }


dictConfig(logging_config)
