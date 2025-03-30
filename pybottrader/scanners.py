"""
Report signal reversions for a set of strategies
"""

from typing import List
from datetime import datetime
from .datastreamers import DataStreamer
from .strategies import Strategy, StrategySignal, Position


class Scanner:
    """The scanner class"""

    datastream: DataStreamer
    strategies: List[Strategy]
    strat_names = List[str]
    last_result: List[StrategySignal] = []

    def __init__(self, strategies: list[Strategy], datastream: DataStreamer):
        self.datastream = datastream
        self.strategies = strategies
        self.strat_names = [type(strategy).__name__ for strategy in self.strategies]

    def next(self) -> bool:
        """The next iteration"""
        obs = self.datastream.next()
        if obs is None:
            return False
        self.last_result = []
        for i, strat in enumerate(self.strategies):
            signal = strat.evaluate(data=obs)
            signal.name = self.strat_names[i]
            signal.symbol = self.datastream.symbol
            self.last_result.append(signal)
        return True

    def status(self) -> List[StrategySignal]:
        """The last result"""
        return self.last_result

    def run(self):
        """A default runner"""
        print(
            "{:19} {:20} {:8} {:>10} {:4}".format(  # pylint: disable=consider-using-f-string
                "Time", "Strategy", "Symbol", "Price", "Position"
            )
        )
        while self.next():
            for signal in self.status():
                if signal.position != Position.STAY:
                    time = datetime.utcfromtimestamp(signal.time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    print(
                        f"{time} "
                        + f"{signal.name:20} "
                        + f"{signal.symbol:8} "
                        + f"{signal.price:10.2f} "
                        + f"{signal.position.name:4} "
                    )
