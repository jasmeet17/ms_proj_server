import logging

LOG_FOLDER = 'static/logs/'

class Logs(object):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create the Handler for logging data to a file
    logger_handler = logging.FileHandler(LOG_FOLDER + 'debugging_logs.log')

    """docstring for Logs"""
    def __init__(self, arg):
        super(Logs, self).__init__()
        self.arg = arg

    """Prints the Logs"""
    @staticmethod
    def printLogs():


        # logger_handler.setLevel(logging.DEBUG)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        # Add the Formatter to the Handler
        Logs.logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        Logs.logger.addHandler(Logs.logger_handler)
        Logs.logger.debug('Completed configuring logger()!')
