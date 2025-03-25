from abc import ABC, abstractmethod
from typing import Callable


class AbstractConnector(ABC):
    """
    Abstract base class for market connectors.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_hooks(self, message_hook: Callable, error_hook: Callable, close_hook: Callable):
        pass

    @abstractmethod
    def get_initial_data(self) -> dict:
        pass
