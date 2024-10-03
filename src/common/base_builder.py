
import logging


# BaseBuilder class provides a foundation for other builder classes
# with basic logging functionality
class BaseBuilder:
    def __init__(self):
        self.logger = None

