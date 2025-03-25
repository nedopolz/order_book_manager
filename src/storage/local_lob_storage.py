import logging

from sortedcontainers import SortedDict

from src.storage.base_storage import AbstractLobStorage

logger = logging.getLogger(__name__)


class LocalLobStorage(AbstractLobStorage):
    """
    Local storage for Limit Order Book data.
    """

    def __init__(self) -> None:
        """
        Simple initialization
        """
        self.bids = SortedDict(lambda x: -float(x))
        self.asks = SortedDict(lambda x: float(x))
        self.last_update_id = None
        self.previous_update_u = None
        self.reboot = False
        self.events = []

    def start(self, initial_data: dict) -> None:
        """
        Real initialization with initial data and processes any queued events
        """
        self.reboot = False
        self.last_update_id = initial_data["lastUpdateId"]
        self.previous_update_u = None

        for price, qty in initial_data.get("bids", []):
            self.bids[price] = float(qty)

        for price, qty in initial_data.get("asks", []):
            self.asks[price] = float(qty)

        for event in self.events:
            self.process_event(event)
        self.events = []

    def process_event(self, event: dict) -> None:
        """
        Processes a single depth update event.
        Rules:
          - Drops any event where u < last_update_id.
          - The first processed event must satisfy U <= last_update_id <= u.
          - If event["pu"] is not equal to the previous event's "u", marks storage for reboot.
          - Updates bids and asks: removes the level if quantity is 0, else updates it.
        """
        if self.last_update_id is None:
            # If storage is not yet initialized, queue the event.
            self.events.append(event)
            return

        if not event.get("e"):
            return

        if event["u"] < self.last_update_id:
            return

        if self.previous_update_u is None:
            if event["U"] > self.last_update_id or event["u"] < self.last_update_id:
                return
        else:
            if event["pu"] != self.previous_update_u:
                logger.info(f"Event consistency broken for event {event}, triggering reboot.")
                self.reboot = True
                return

        for price, qty in event.get("b", []):
            if float(qty) == 0:
                self.bids.pop(price, None)
            else:
                self.bids[price] = float(qty)

        for price, qty in event.get("a", []):
            if float(qty) == 0:
                self.asks.pop(price, None)
            else:
                self.asks[price] = float(qty)

        self.previous_update_u = event["u"]
        self.last_update_id = event["u"]

    def need_reboot(self) -> bool:
        """
        Indicates if reboot is needed.
        """
        return self.reboot

    def get_bids(self) -> SortedDict:
        """
        Returns the current bids.
        """
        return self.bids

    def get_asks(self) -> SortedDict:
        """
        Returns the current asks.
        """
        return self.asks
