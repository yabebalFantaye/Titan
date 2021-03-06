from core.database import ohlcv_functions
from core.database import database
from ta.base_indicator import BaseIndicator

engine = database.engine
conn = engine.connect()

class VolumeChangeMonitor(BaseIndicator):
    def __init__(self, market, interval):
        super(VolumeChangeMonitor, self).__init__(market, interval, 2)
        self.__previous_volume = 0
        self.close = None
        self.timestamp = None
        self.value = None

    def next_calculation(self, candle):
        """get latest N candles from market, do calculation, write results to db"""
        self.do_calculation(candle)

    def do_calculation(self, candle):
        new_volume = candle[5]
        if self.__previous_volume is not 0:
            self.value = round(100 * ((new_volume - self.__previous_volume)/self.__previous_volume), 2)  # calculate change in volume in percentage terms
        self.__previous_volume = new_volume
        self.timestamp = ohlcv_functions.convert_timestamp_to_date(candle[0])
        self.close = candle[4]

