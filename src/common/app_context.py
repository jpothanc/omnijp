from typing import Optional, Callable

class AppContext:
    def __init__(self):
        self._logger: Optional[Callable] = None

    @property
    def logger(self) -> Optional[Callable]:
        return self._logger

    @logger.setter
    def logger(self, value: Optional[Callable]):
        self._logger = value