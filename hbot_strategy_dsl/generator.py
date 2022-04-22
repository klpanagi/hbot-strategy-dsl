# Copyright (c) 2021, Panayiotou, Konstantinos <klpanagi@gmail.com>
# Author: Panayiotou, Konstantinos <klpanagi@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from textx import generator, textx_isinstance
from os import path, mkdir, getcwd, chmod
import jinja2
import re

from .language import build_model

_THIS_DIR = path.abspath(path.dirname(__file__))

SRC_GEN_DIR = path.join(path.realpath(getcwd()), 'gen')

# Initialize template engine.
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.join(_THIS_DIR, 'templates')),
    trim_blocks=True,
    lstrip_blocks=True
)


def camelcase_to_snakecase(_str: str) -> str:
    """camelcase_to_snakecase.
    Transform a camelcase string to  snakecase
    Args:
        _str (str): String to apply transformation.
    Returns:
        str: Transformed string
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', _str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def set_defaults(strategy):
    # for p in strategy.parameters:
    #     p.description = p.description.split('#')[1].strip()
    if strategy.author in (None, ""):
        strategy.author = "Anonymous"
    if strategy.description in (None, ""):
        strategy.description = "TODO"
    # if strategy.type is None:
    #     strategy.type
    return strategy


# From: StrategyBase ---------------------------------------------->

CONF_TEMPLATE_TPL = jinja_env.get_template('strategy_base/strategy_conf.tpl')
CONF_MAP_TPL = jinja_env.get_template('strategy_base/strategy_conf_map.tpl')
START_TPL = jinja_env.get_template('strategy_base/strategy_start.tpl')
STRATEGY_TPL = jinja_env.get_template('strategy_base/strategy_impl.tpl')


def generate_init_file(strategy, out_dir: str):
    out_file = path.join(out_dir, "__init__.py")
    with open(path.join(out_file), 'w') as f:
        f.write(f"# Author: {strategy.author}")
        f.write(f"# Author Email: {strategy.authorEmail}")
    chmod(out_file, 509)


def generate_strategy_file(strategy, out_dir: str):
    strategy_name = camelcase_to_snakecase(strategy.name)
    strategy.name_snake = strategy_name
    out_file = path.join(out_dir, f"{strategy_name}.py")
    with open(path.join(out_file), 'w') as f:
        f.write(STRATEGY_TPL.render(strategy=strategy))
    chmod(out_file, 509)


def generate_start_file(strategy, out_dir: str):
    strategy_name = camelcase_to_snakecase(strategy.name)
    strategy.name_snake = strategy_name
    out_file = path.join(out_dir, "start.py")
    with open(path.join(out_file), 'w') as f:
        f.write(START_TPL.render(strategy=strategy))
    chmod(out_file, 509)


def generate_conf_map_file(strategy, out_dir: str):
    strategy_name = camelcase_to_snakecase(strategy.name)
    strategy.name_snake = strategy_name
    out_file = path.join(out_dir,
                         f"{strategy_name}_config_map.py")
    with open(path.join(out_file), 'w') as f:
        f.write(CONF_MAP_TPL.render(strategy=strategy))
    chmod(out_file, 509)


def generate_conf_tpl_file(strategy, out_dir: str):
    strategy_name = camelcase_to_snakecase(strategy.name)
    out_file = path.join(
        out_dir,
        f"conf_{strategy_name}_strategy_TEMPLATE.yml"
    )
    with open(path.join(out_file), 'w') as f:
        f.write(CONF_TEMPLATE_TPL.render(strategy=strategy))
    chmod(out_file, 509)


def generate_strategy_base(model, out_dir: str = '') -> str:
    # Create output folder
    if out_dir in (None, ''):
        out_dir = SRC_GEN_DIR
    if not path.exists(out_dir):
        mkdir(out_dir)

    strategy = set_defaults(model)

    generate_conf_tpl_file(strategy, out_dir)
    generate_conf_map_file(strategy, out_dir)
    generate_init_file(strategy, out_dir)
    generate_start_file(strategy, out_dir)
    generate_strategy_file(strategy, out_dir)

    return out_dir

# ------------------------------------------------------------------

# From: ScriptStrategyBase ---------------------------------------->

SCRIPT_STRATEGY_TPL = jinja_env.get_template(
    'script_strategy/strategy_impl.tpl'
)


def generate_script_strategy(model, out_dir: str = '') -> str:
    if out_dir in (None, ''):
        out_dir = SRC_GEN_DIR
    if not path.exists(out_dir):
        mkdir(out_dir)

    strategy = set_defaults(model)
    strategy_name = camelcase_to_snakecase(strategy.name)
    return out_dir

# ------------------------------------------------------------------

def generate_from_model(model_fpath: str):
    model = build_model(model_fpath)
    print(model.strategy)
    return generate_strategy_base(model)


@generator('hummingbot', 'v3')
def code_generator(metamodel, model, output_path, overwrite,
        debug: bool, **custom_args):
    """code_generator.

    Args:
        metamodel:
        model:
        output_path:
        overwrite:
        debug (bool): debug
        custom_args:
    """
    generate_from_model(model._tx_filename)
