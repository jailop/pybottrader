"""Data Streamers"""

from typing import Union
import pandas as pd
import yfinance


class DataStreamer:
    """A data streamer abstract class"""

    def __init__(self):
        """Init method"""

    def next(self) -> Union[dict, None]:
        """Next method"""


class YFinanceStreamer(DataStreamer):
    """Using Yahoo Finance to retrieve data"""

    index = 0
    data: pd.DataFrame

    def __init__(self, symbol, *args, **kwargs):
        super().__init__()
        ticker = yfinance.Ticker(symbol)
        self.data = ticker.history(*args, **kwargs)
        self.data.rename(
            columns={
                "Open": "open",
                "Close": "close",
                "High": "high",
                "Low": "low",
                "Volume": "volume",
            },
            inplace=True,
        )
        self.data.index.names = ["time"]
        self.data.reset_index(inplace=True)

    def next(self) -> Union[dict, None]:
        if self.index >= len(self.data):
            return None
        result = self.data.iloc[self.index].to_dict()
        result["time"] = result["time"].to_pydatetime()
        self.index += 1
        return result


class CSVFileStreamer(DataStreamer):
    """
    An dataframe file streamer
    """

    data: pd.DataFrame
    index: int

    def __init__(self, filename: str):
        self.index = 0
        self.data = pd.read_csv(filename, parse_dates=True)

    def next(self) -> Union[dict, None]:
        if self.index >= len(self.data):
            return None
        result = self.data.iloc[self.index].to_dict()
        self.index += 1
        return result
