import json
from json import JSONDecodeError
import logging
import threading
import time

from src.connectors.base_connector import AbstractConnector
from src.storage.base_storage import AbstractLobStorage

logger = logging.getLogger(__name__)


class BaseController:
    """
    Simple controller for connector and storage
    """

    def __init__(self, connector: AbstractConnector, storage: AbstractLobStorage):
        """
        Initializes the controller by setting hooks and starting reboot observation.
        """
        self.connector = connector
        self.storage = storage
        self.connector.set_hooks(
            self.event_hook, self.error_hook, self.closed_hook
        )  # at first set hook to start storing events
        self.storage.start(self.connector.get_initial_data())  # than init storage
        threading.Thread(target=self.observe, daemon=True).start()

    def event_hook(self, _, event):
        """
        Handles incoming market data events.
        """
        try:
            data = json.loads(event)
            self.storage.process_event(data)
        except JSONDecodeError as e:
            logger.exception(f"Failed to process event: {e}")

    def error_hook(self, *args, **kwargs):
        """
        Handles errors from the connector.
        """
        logger.error(f"Error {args}, {kwargs}")
        self.handle_reboot()

    def closed_hook(self, *args, **kwargs):
        """
        Handles connection closures.
        """
        logger.error(f"Connection closed {args}, {kwargs}")
        self.handle_reboot()

    def handle_reboot(self):
        """
        Reboots storage and observation thread.
        """
        self.storage.start(self.connector.get_initial_data())
        threading.Thread(target=self.observe, daemon=True).start()

    def observe(self):
        """
        Checks if storage needs to be rebooted.
        """
        while True:
            if self.storage.need_reboot():
                logger.info("BaseController: Reboot detected!")
                self.handle_reboot()
                break
            time.sleep(0.01)  # update time is 100ms so we had plenty of time
