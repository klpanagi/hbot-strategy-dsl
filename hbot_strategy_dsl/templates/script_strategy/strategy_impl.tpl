import logging
import time
from decimal import Decimal
from statistics import mean
from typing import List

from hummingbot.connector.exchange_base import ExchangeBase
from hummingbot.connector.utils import split_hb_trading_pair
from hummingbot.core.data_type.order_candidate import OrderCandidate
from hummingbot.core.event.events import OrderFilledEvent, OrderType, TradeType
from hummingbot.core.rate_oracle.rate_oracle import RateOracle
from hummingbot.strategy.script_strategy_base import ScriptStrategyBase


NaN = float("nan")
s_decimal_zero = Decimal(0)
s_decimal_nan = Decimal("NaN")
lms_logger = None


class {{ strategy.name }}(ScriptStrategyBase):
{% for param in strategy.parameters %}
    {{ param.name }}: {{ param.type }},
{% endfor %}


    @property
    def connector(self) -> ExchangeBase:
        """
        The only connector in this strategy, define it here for easy access
        """
        return self.connectors[self.connector_name]

    def on_tick(self):
        """
        Runs every tick_size seconds, this is the main operation of the strategy.
        - Create proposal (a list of order candidates)
        - Check the account balance and adjust the proposal accordingly (lower order amount if needed)
        - Lastly, execute the proposal on the exchange
        """
        proposal: List[OrderCandidate] = self.create_proposal()
        proposal = self.connector.budget_checker.adjust_candidates(proposal, all_or_none=False)
        if proposal:
            self.execute_proposal(proposal)

    def execute_proposal(self, proposal: List[OrderCandidate]):
        """
        Places the order candidates on the exchange, if it is not within cool off period and order candidate is valid.
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
        Creates and returns a proposal (a list of order candidate), in this strategy the list has 1 element at most.
        """
        proposal = []
        # If the current price (the last close) is below the dip, add a new order candidate to the proposal
        order_price = self.connector.get_price(
                self.trading_pair, False) * Decimal("0.9")
        usd_conversion_rate = RateOracle.get_instance().rate(
                self.conversion_pair)
        amount = (self.buy_usd_amount / usd_conversion_rate) / order_price
        proposal.append(
            OrderCandidate(
                self.trading_pair,
                False,
                OrderType.LIMIT,
                TradeType.BUY,
                amount,
                order_price
            )
        )
        return proposal

