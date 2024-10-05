import logging


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        # return record.getMessage().find("/healthcheck") == -1

        if (record.args and len(record.args) >= 2):
            request_method = record.args[1]
            query_string = record.args[2]
            return request_method == 'GET' and not query_string in [
                "/healthcheck",
            ]
        else:
            return True


def get_logging_config():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "healthcheckfilter": {
                "()": HealthCheckFilter,
            }
        },
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "filters": ["healthcheckfilter"],
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout",  # Log to standard output
            },
            # "file": {
            #     "class": "logging.FileHandler",
            #     "filters": ["healthcheckfilter"],
            #     "level": "DEBUG",  # Log level for file
            #     "formatter": "default",
            #     "filename": "app.log",  # Log to app.log file
            # },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "fastapiproject": {  # Custom logger for this application
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {  # Uvicorn error logs
                "level": "INFO",  # Set to WARNING to suppress INFO logs
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {  # Uvicorn access logs
                "level": "WARNING",  # Set to WARNING to suppress INFO logs
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }
    return log_config
