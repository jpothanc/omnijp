
import logging


# BaseBuilder class provides a foundation for other builder classes
# with basic logging functionality
class BaseBuilder:
    def __init__(self):
        self.logger = None

    def _create_default_console_logger(self):
        print("create_logger")
        self.logger = logging.getLogger(__name__)
        # With this setting, the logger will output messages for all levels: DEBUG, INFO, WARNING, ERROR, and CRITICAL.
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


