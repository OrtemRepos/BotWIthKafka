from abc import ABC, abstractmethod


class ExchangeRate(ABC):
    @abstractmethod
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        raise NotImplementedError


class FakeExchangeRate(ExchangeRate):
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        return 100.0
