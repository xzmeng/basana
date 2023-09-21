import basana as bs

from talipp.indicators import SMA

class Strategy(bs.TradingSignalSource):
    def __init__(self, dispatcher: bs.EventDispatcher, fast_period: float, slow_period: float):
        super().__init__(dispatcher)

        self.slow_sma = SMA(slow_period)
        self.fast_sma = SMA(fast_period)

    async def on_bar_event(self, bar_event: bs.BarEvent):
        value = float(bar_event.bar.close)

        self.slow_sma.add_input_value(value)
        self.fast_sma.add_input_value(value)

        if len(self.slow_sma) < 2 or len(self.fast_sma) < 2:
            return

        if self.fast_sma[-1] > self.slow_sma[-1] and self.fast_sma[-2] < self.slow_sma[-2]:
            # cross up
            self.push(bs.TradingSignal(bar_event.when, bs.OrderOperation.BUY, bar_event.bar.pair))

        elif self.fast_sma[-1] < self.slow_sma[-1] and self.fast_sma[-2] > self.slow_sma[-2]:
            # cross down
            self.push(bs.TradingSignal(bar_event.when, bs.OrderOperation.SELL, bar_event.bar.pair))




