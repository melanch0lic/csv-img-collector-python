LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
                # 'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s\n%(data)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'wiki_log_file': {
                #'class': 'cloghandler.ConcurrentRotatingFileHandler',
                'class': 'logging.StreamHandler',
                'filename': 'logs/wiki.log', # os.path.join(LOG_ROOT, 'main.log'),
                'encoding': 'utf-8',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 10,
                'formatter': 'verbose',
                # 'filters': ['format_data'],
            },
            'ccsearch_log_file': {
                #'class': 'cloghandler.ConcurrentRotatingFileHandler',
                'class': 'logging.StreamHandler',
                'filename': 'logs/ccsearch.log', # os.path.join(LOG_ROOT, 'main.log'),
                'encoding': 'utf-8',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 10,
                'formatter': 'verbose',
                # 'filters': ['format_data'],
            },
            'brit_log_file': {
                #'class': 'cloghandler.ConcurrentRotatingFileHandler',
                'class': 'logging.StreamHandler',
                'filename': 'logs/britannica.log', # os.path.join(LOG_ROOT, 'main.log'),
                'encoding': 'utf-8',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 10,
                'formatter': 'verbose',
                # 'filters': ['format_data'],
            },
            'pexels_log_file': {
                #'class': 'cloghandler.ConcurrentRotatingFileHandler',
                'class': 'logging.StreamHandler',
                'filename': 'logs/pexels.log', # os.path.join(LOG_ROOT, 'main.log'),
                'encoding': 'utf-8',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 10,
                'formatter': 'verbose',
                # 'filters': ['format_data'],
            },
            'console': {
                'level': 'DEBUG',  # WARN
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
        'brit': {
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