LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'wiki_log_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/wiki.log',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'ccsearch_log_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/ccsearch.log',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'brit_log_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/britannica.log',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'pexels_log_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/pexels.log',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'wiki': {
            'level': 'DEBUG',
            'handlers': ['console', 'wiki_log_file'],
            'propagate': False
        },
        'ccsearch': {
            'level': 'DEBUG',
            'handlers': ['console', 'ccsearch_log_file'],
            'propagate': False
        },
        'britannica': {
            'level': 'DEBUG',
            'handlers': ['console', 'brit_log_file'],
            'propagate': False
        },
        'pexels': {
            'level': 'DEBUG',
            'handlers': ['console', 'pexels_log_file'],
            'propagate': False
        }
    }
}