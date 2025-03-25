from abc import ABC, abstractmethod


class AbstractCalculation(ABC):
    """
    Abstract base class for performing calculations
    """

    @abstractmethod
    def calc_metric(self, *args, **kwargs):
        pass

    @abstractmethod
    def save_metric(self, data: dict):
        pass
