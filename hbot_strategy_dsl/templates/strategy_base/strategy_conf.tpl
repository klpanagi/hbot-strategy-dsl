########################################################
###        {{ strategy.name  }} strategy config      ###
########################################################

template_version: 3
strategy: null

{% for param in strategy.parameters %}

# {{ param.description  }}
{{ param.name }}: {{param.defaultValue}}
{% endfor %}
