"""
Moving Average
Implementation adopted from:
https://github.com/jailop/trading/tree/main/indicators-c++
"""

import numpy as np


class Indicator:
    """
    Base class to build indicators. It provides a buffer to
    keep the last `mem_size` values and functions to push
    new values and retrieve using bracket notation or the
    function get.

    All derived classes, call the __init__ method of this class
    and when an update ocurrs, they push the new value
    into the memory buffer.

    Because this class is intended to be used for time series,
    indices go backwards, being `0` the last updated value, -1
    the previous one, -2 the previous of the previos one...
    If a value is requested with a positive index or a negative
    index which absolute values is greater than `mem_size`, then
    an NAN value is returned.
    """

    mem_pos: int
    mem_data: np.ndarray
    mem_size: int

    def __init__(self, mem_size=1):
        """
        @param mem_size: The size of the memory buffer. The
            default value is 1.
        """
        self.mem_data = np.empty((mem_size,))
        self.mem_data[:] = np.nan
        self.mem_pos = 0
        self.mem_size = mem_size

    def __getitem__(self, key):
        """
        @param key: 0 for the most recent update
                    a negative number for the n-previous updates

        A negative number less than -mem_size returns NAN.
        A positive number returns NAN.
        """
        if key > 0 or -key >= self.mem_size:
            return np.nan
        real_pos = (self.mem_pos - key) % self.mem_size
        return self.mem_data[real_pos]

    def push(self, value):
        """
        Stores in the buffer `value` as the more recent update.
        In the current implementation, a ring buffer is used
        to save these values.

        @param value: The most recent update
        """
        self.mem_pos = (self.mem_pos - 1) % self.mem_size
        self.mem_data[self.mem_pos] = value

    def get(self, key=0) -> float:
        """The same as `__getitem__`"""
        return self[key]


class MA(Indicator):
    """Moving Average"""

    period: int
    prevs: np.ndarray
    length: int = 0
    pos: int = 0
    accum: float = 0.0

    def __init__(self, period: int, *args, **kwargs):
        """
        The number of period or window size is required to initialize a MA
        object.
        """
        super().__init__(*args, **kwargs)
        self.period = period
        self.prevs = np.zeros(period, dtype=float)

    def update(self, value: float) -> float:
        """Aggregate a new value into the moving average"""
        if self.length < self.period:
            self.length += 1
        else:
            self.accum -= self.prevs[self.pos]
        self.prevs[self.pos] = value
        self.accum += value
        self.pos = (self.pos + 1) % self.period
        if self.length < self.period:
            self.push(np.nan)
        else:
            self.push(self.accum / self.period)
        return self[0]


class EMA(Indicator):
    """Exponential Moving Average"""

    periods: float
    alpha: float
    smooth_factor: float
    length: int = 0
    prev: float = 0.0

    def __init__(self, periods: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        alpha = 2.0 if "alpha" not in kwargs else kwargs["alpha"]
        self.periods = periods
        self.alpha = alpha
        self.smooth_factor = alpha / (1.0 + periods)

    def update(self, value: float) -> float:
        """Aggregate a new value into the moving average"""
        self.length += 1
        if self.length < self.periods:
            self.prev += value
        elif self.length == self.periods:
            self.prev += value
            self.prev /= self.periods
        else:
            self.prev = (value * self.smooth_factor) + self.prev * (
                1.0 - self.smooth_factor
            )
        if self.length < self.periods:
            self.push(np.nan)
        else:
            self.push(self.prev)
        return self[0]


class ROI(Indicator):
    """
    Return of investment for streaming data.
    """

    prev: float

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev = np.nan

    def update(self, value: float) -> float:
        """
        Updates the indicator. If at least
        a previous value has been updated before,
        it starts reporting the return of the
        investment.
        """
        curr = roi(self.prev, value)
        self.push(curr)
        self.prev = value
        return self[0]


def roi(initial_value, final_value):
    """Return on investment"""
    if initial_value == 0 or np.isnan(initial_value):
        return np.nan
    return final_value / initial_value - 1.0
