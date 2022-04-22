"""
<This is a {{ strategy.type }} strategy generated using the hbot-strategy-dsl>

Description: {{ strategy.description }}
Author: {{ strategy.author }}

"""

import time
import logging
from decimal import Decimal
from statistics import mean
from typing import List

from hummingbot.connector.exchange_base import ExchangeBase
from hummingbot.connector.utils import split_hb_trading_pair
from hummingbot.core.data_type.order_candidate import OrderCandidate
from hummingbot.core.event.events import OrderFilledEvent, OrderType, TradeType
from hummingbot.core.rate_oracle.rate_oracle import RateOracle
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase


class {{ strategy.name }}(ScriptStrategyBase):
    """
    {{ strategy.description }}
    """

{% for param in strategy.parameters %}
    {{ param.name }}: {{ param.type }} = {{ param.defaultValue }}
{% endfor %}

    markets =  {
{% for market in strategy.markets %}
        '{{ market.connector }}': {{ market.pairs }},
{% endfor %}
    }

    @property
    def logger(self):
        return self.logger()

    def on_tick(self):
        """
        Runs every tick_size seconds, this is the main operation
        of the strategy.
        - Create proposal (a list of order candidates)
        - Check the account balance and adjust the proposal accordingly
          (lower order amount if needed)
        - Lastly, execute the proposal on the exchange
        """
        proposal: List[OrderCandidate] = self.create_proposal()
        proposal = self.connector.budget_checker.adjust_candidates(
                proposal, all_or_none=False)
        if proposal:
            self.execute_proposal(proposal)

    def execute_proposal(self, proposal: List[OrderCandidate]):
        """
        Places the order candidates on the exchange, if it is not within cool
        off period and order candidate is valid.
        """
        if self.last_ordered_ts > time.time() - self.cool_off_interval:
            return
        for order_candidate in proposal:
            if order_candidate.amount > Decimal("0"):
                self.buy(
                    self.connector_name,
                    self.trading_pair,
                    order_candidate.amount,
                    order_candidate.order_type,
                    order_candidate.price
                )
                self.last_ordered_ts = time.time()

    def create_proposal(self) -> List[OrderCandidate]:
        """
        Creates and returns a proposal (a list of order candidate), in this
        strategy the list has 1 element at most.
        """
        proposal = []
        order_price = self.connector.get_price(
                self.trading_pair, False) * Decimal("1.0")
        proposal.append(
            OrderCandidate(
                self.trading_pair,
                False,
                OrderType.LIMIT,
                TradeType.BUY,
                0,
                order_price
            )
        )
        return proposal

    def did_fill_order(self, event: OrderFilledEvent):
        """
        Listens to fill order event to log it and notify the hummingbot
        application.
        If you set up Telegram bot, you will get notification there as well.
        """
        msg = (f"({event.trading_pair}) {event.trade_type.name} "
               f"order (price: {event.price}) of {event.amount} "
               f"{split_hb_trading_pair(event.trading_pair)[0]} is filled.")
        self.logger.info(msg)
        self.notify_hb_app_with_timestamp(msg)
