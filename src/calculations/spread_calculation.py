import csv
import logging
import os
import time

from src.calculations.base_calculation import AbstractCalculation
from src.controllers.base_controller import BaseController

logger = logging.getLogger(__name__)


class SpreadCalculation(AbstractCalculation):
    """
    Implements given formula, save data to CSV file
    """

    def __init__(self, controller: BaseController, file_name: str):
        self.controller = controller
        self.file_name = file_name

    def calc_metric(self):
        """
        Calculates the spread metric and saves it
        """
        try:
            second_best_ask = float(self.controller.storage.get_asks().peekitem(1)[0])
            second_best_bid = float(self.controller.storage.get_bids().peekitem(1)[0])
        except Exception as e:
            logger.error(f"Error accessing LOB data: {e}")
            return

        spread = 2 * ((second_best_ask - second_best_bid) / (second_best_ask + second_best_bid))
        self.save_metric(spread)

    def save_metric(self, spread: float):
        """
        Saves the spread metric to csv file
        """
        file_exists = os.path.exists(self.file_name)
        with open(self.file_name, "a+", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["timestamp", "instrument", "metric"])
            writer.writerow([time.time(), self.__class__.__name__, spread])
