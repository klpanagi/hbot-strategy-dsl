from decimal import Decimal
import logging
import asyncio
from hummingbot.core.clock import Clock
from hummingbot.logger import HummingbotLogger
from hummingbot.strategy.strategy_py_base import StrategyPyBase


NaN = float("nan")
s_decimal_zero = Decimal(0)
s_decimal_nan = Decimal("NaN")
lms_logger = None


class {{ strategy.name }}(StrategyPyBase):

    @classmethod
    def logger(cls) -> HummingbotLogger:
        global lms_logger
        if lms_logger is None:
            lms_logger = logging.getLogger(__name__)
        return lms_logger

    def init_params(self,
{% for param in strategy.parameters %}
                    {{ param.name }}: {{ param.type }},
{% endfor %}
                    status_report_interval: float = 900,
                    hb_app_notification: bool = False):

{% for param in strategy.parameters %}
        self._{{ param.name }} = {{ param.name }}
{% endfor %}

        self._ev_loop = asyncio.get_event_loop()
        self._last_timestamp = 0
        self._status_report_interval = status_report_interval
        self._ready_to_trade = False
        self._refresh_time = 0
        self._hb_app_notification = hb_app_notification

    @property
    def active_orders(self):
        """
        List active orders (they have been sent to the market and have not been cancelled yet)
        """
        limit_orders = self.order_tracker.active_limit_orders
        return [o[1] for o in limit_orders]

    def tick(self, timestamp: float):
        """
        Clock tick entry point, is run every second (on normal tick setting).
        :param timestamp: current tick timestamp
        """
        ## HERE GOES THE IMPLEMENTATION OF THE LOGIC OF THE STRATEGY
        ##
        ## TODO: ADD A SINGLE EXAMPLE
        self._last_timestamp = timestamp

    def start(self, clock: Clock, timestamp: float):
        ## TODO
        pass

    def stop(self, clock: Clock):
        ## TODO
        pass

    def notify_hb_app(self, msg: str):
        """
        Send a message to the hummingbot application
        """
        if self._hb_app_notification:
            super().notify_hb_app(msg)
