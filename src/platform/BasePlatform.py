from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePlatform(ABC):
    @abstractmethod
    def get_connection_status(self) -> str:
        """Return connection status: 'connected', 'disconnected', etc."""
        pass

    @abstractmethod
    def fetch_data(self) -> Any:
        """Fetch raw or preprocessed data from the platform (e.g., OHLCV)."""
        pass

    @abstractmethod
    def send_signal(self, signal: Dict[str, Any]) -> None:
        """Send an order or trading signal to the exchange."""
        pass

    @abstractmethod
    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """Validate that the signal is structurally correct and executable."""
        pass
