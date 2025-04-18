"""
Financial indicators for streaming data implemented in C++
"""

from __future__ import annotations

__all__ = [
    "ATR",
    "EMA",
    "FloatIndicator",
    "MA",
    "MACD",
    "MACDIndicator",
    "MACDResult",
    "MV",
    "ROI",
    "RSI",
    "roi",
]

class ATR(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, period: int, mem_size: int = 1) -> None: ...
    def update(
        self, low_price: float, high_price: float, close_price: float
    ) -> float: ...

class EMA(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, period: int, alpha: float = 2.0, mem_size: int = 1) -> None: ...
    def update(self, arg0: float) -> float: ...

class FloatIndicator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __getitem__(self, arg0: int) -> float: ...
    def __init__(self, mem_size: int = 1) -> None: ...
    def get(self, key: int = 0) -> float: ...
    def push(self, arg0: float) -> None: ...

class MA(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, period: int, mem_size: int = 1) -> None: ...
    def update(self, arg0: float) -> float: ...

class MACD(MACDIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, short_period: int, long_period: int, diff_period: int, mem_size: int = 1
    ) -> None: ...
    def update(self, arg0: float) -> MACDResult: ...

class MACDIndicator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __getitem__(self, arg0: int) -> ...: ...
    def __init__(self, mem_size: int = 1) -> None: ...
    def get(self, key: int = 0) -> ...: ...
    def push(self, arg0: ...) -> None: ...

class MACDResult:
    hist: float
    macd: float
    signal: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...

class MV(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, period: int, mem_size: int = 1) -> None: ...
    def update(self, arg0: float) -> float: ...

class ROI(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, mem_size: int = 1) -> None: ...
    def update(self, arg0: float) -> float: ...

class RSI(FloatIndicator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, period: int = 14, mem_size: int = 1) -> None: ...
    def update(self, open_price: float, close_price: float) -> float: ...

def roi(arg0: float, arg1: float) -> float:
    """
    Calculate return on investment
    """
