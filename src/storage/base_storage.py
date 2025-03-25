from abc import ABC, abstractmethod
from collections.abc import MutableMapping


class AbstractLobStorage(ABC):
    """
    Abstract base class for Limit Order Book storage.
    """

    @abstractmethod
    def process_event(self, event: dict):
        pass

    @abstractmethod
    def start(self, initial_data: dict):
        pass

    @abstractmethod
    def need_reboot(self) -> bool:
        pass

    @abstractmethod
    def get_bids(self) -> MutableMapping:
        pass

    @abstractmethod
    def get_asks(self) -> MutableMapping:
        pass
