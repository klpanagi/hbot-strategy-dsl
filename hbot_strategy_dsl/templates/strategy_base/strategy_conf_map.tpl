"""
The configuration parameters for a user made liquidity_mining strategy.
"""

import re
from decimal import Decimal
from typing import Optional
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_validators import (
    validate_exchange,
    validate_decimal,
    validate_int,
    validate_bool
)

{{ strategy.name_snake }}_config_map = {
    "strategy":
        ConfigVar(
            key="strategy",
            prompt="",
            default="{{ strategy.name_snake }}"
        ),
{% for param in strategy.parameters %}
    "{{ param.name }}":
        ConfigVar(
            key="{{ param.name }}",
            prompt="",
            type_str="{{ param.type }}",
            default={{ param.defaultValue }}
        ),
{% endfor %}
}
