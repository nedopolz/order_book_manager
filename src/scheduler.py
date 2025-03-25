import datetime
import logging
import threading
import time

from src.calculations.base_calculation import AbstractCalculation

logger = logging.getLogger(__name__)


class Scheduler:
    """
    Runs calculation periodically based on provided frequency.
    """

    def __init__(self, frequency_minutes: int, calculation: AbstractCalculation) -> None:
        """
        Initializes and starts scheduling thread.
        """
        self.frequency = frequency_minutes
        self.calculation = calculation
        self._stop_event = threading.Event()
        threading.Thread(target=self.run, daemon=True, name="SchedulerThread").start()

    def calculate_sleep_time(self) -> tuple[float, datetime.datetime]:
        """
        Calculates sleep time until next calculation.
        """
        now = datetime.datetime.now()
        next_minute_block = (now.minute // self.frequency + 1) * self.frequency

        if next_minute_block >= 60:
            next_trigger = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        else:
            next_trigger = now.replace(minute=next_minute_block, second=0, microsecond=0)

        sleep_time = (next_trigger - now).total_seconds()
        return sleep_time, next_trigger

    def run(self) -> None:
        """
        Sleep until next trigger time and then execute calculation.
        """
        while not self._stop_event.is_set():
            sleep_time, next_trigger = self.calculate_sleep_time()
            logger.info("Scheduler: Sleeping for %.2f seconds until %s.", sleep_time, next_trigger.time())
            time.sleep(sleep_time)
            try:
                self.calculation.calc_metric()
                logger.info("Scheduler: Calculation triggered at %s", datetime.datetime.now().time())
            except Exception as e:
                logger.exception("Scheduler: Error during calculation - %s", e)

    def stop(self) -> None:
        """
        Stops scheduler loop.
        """
        self._stop_event.set()
