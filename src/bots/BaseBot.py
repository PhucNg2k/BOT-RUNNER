from abc import ABC, abstractmethod

class BaseBot(ABC):
    @abstractmethod
    def generate_signal(self, df):
        pass