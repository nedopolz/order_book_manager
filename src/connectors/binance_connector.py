from typing import Callable

from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from src.connectors.base_connector import AbstractConnector


class BinanceConnector(AbstractConnector):

    def __init__(self, symbol: str) -> None:
        """
        symbol: Trading symbol acording to api doc
        """
        self.symbol = symbol
        self.cm_futures_client = UMFutures()

    def set_hooks(self, message_hook: Callable, error_hook: Callable, close_hook: Callable) -> None:
        """
        sets all needed hooks, and creates client
        """
        client = UMFuturesWebsocketClient(on_message=message_hook, on_error=error_hook, on_close=close_hook)
        client.diff_book_depth(symbol=self.symbol)

    def get_initial_data(self) -> dict:
        """
        Retrieves the initial market data.
        """
        return self.cm_futures_client.depth(symbol=self.symbol, limit=1000)
