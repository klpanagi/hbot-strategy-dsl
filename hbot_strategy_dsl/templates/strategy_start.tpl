from decimal import Decimal
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.strategy.{{ strategy.name_snake }}.{{ strategy.name_snake }} import {{ strategy.name }}
from hummingbot.strategy.{{ strategy.name_snake }}.{{ strategy.name_snake }}_config_map import {{ strategy.name_snake }}_config_map as c_map


def start(self):
    try:
{% for param in strategy.parameters %}
        {{ param.name }} = c_map.get("{{ param.name }}").value
{% endfor %}

        self.strategy = {{ strategy.name }}()

        self.strategy.init_params(
{% for param in strategy.parameters %}
            {{ param.name }} = {{ param.name }},
{% endfor %}
            hb_app_notification=True
        )
        self.logger().info('Initialized strategy: SimpleStrategy')
    except Exception as e:
        self._notify(str(e))
        self.logger().error("Error during initialization!!", exc_info=True)
