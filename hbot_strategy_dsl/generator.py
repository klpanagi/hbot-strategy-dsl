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

# Initialize template engine.
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path.join(_THIS_DIR, 'templates')),
    trim_blocks=True,
    lstrip_blocks=True)

template = jinja_env.get_template('strategy_conf.tpl')

srcgen_folder = path.join(path.realpath(getcwd()), 'gen')


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
    return strategy


def generate_conf_tpl_file(strategy, out_dir):
    strategy_name = camelcase_to_snakecase(strategy.name)
    out_file = path.join(out_dir,
                         f"conf_{strategy_name}_strategy_TEMPLATE.yml")
    with open(path.join(out_file), 'w') as f:
        f.write(template.render(strategy=strategy))
    chmod(out_file, 509)

def generate_project(model_fpath: str,
             out_dir: str = None):
    # Create output folder
    if out_dir is None:
        out_dir = srcgen_folder
    model = build_model(model_fpath)
    if not path.exists(out_dir):
        mkdir(out_dir)

    strategy = set_defaults(model)

    generate_conf_tpl_file(strategy, out_dir)

    return out_dir


def generate(model_fpath: str):
    return generate_project(model_fpath)


@generator('hummingbot', 'v3')
def goal_dsl_generate_goalee(metamodel, model, output_path, overwrite, debug, **custom_args):
    "Generator for generating goalee from goal_dsl descriptions"
    generate(model._tx_filename)
