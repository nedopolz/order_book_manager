from src.calculations.spread_calculation import SpreadCalculation
from src.connectors.binance_connector import BinanceConnector
from src.controllers.base_controller import BaseController
from src.scheduler import Scheduler
from src.storage.local_lob_storage import LocalLobStorage


def main() -> None:
    """
    Main entry point to set up and start the scheduler.
    """
    connector = BinanceConnector(symbol="btcusdt")
    storage = LocalLobStorage()
    controller = BaseController(connector=connector, storage=storage)
    spread_calculation = SpreadCalculation(controller=controller, file_name="deleteme.csv")

    scheduler = Scheduler(frequency_minutes=5, calculation=spread_calculation)

    # scheduler.stop()


if __name__ == "__main__":
    main()
