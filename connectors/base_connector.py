from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def parse_data(self, raw_data):
        pass
