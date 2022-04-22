import sys
import os
from os import path, getenv, mkdir, listdir
import shutil
import click

from .generator import generate_from_model as hbot_generator
from .validator import validate_from_file


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command(help='Hummingbot Strategy Project Generator')
@click.pass_context
@click.argument('model_path')
def generate(ctx, model_path: str):
    model_path = str(model_path)
    hbot_generator(model_path)


@cli.command(help='Hummingbot Strategy Project Generator')
@click.pass_context
@click.argument('model_path')
def validate(ctx, model_path: str):
    model_path = str(model_path)
    validate_from_file(model_path)


@cli.command(help='Hummingbot Strategy Project Generator')
@click.pass_context
@click.argument('strategy_gen_dir')
@click.argument('strategy_name')
def build(ctx, strategy_gen_dir: str, strategy_name: str):
    hummingbot_repo_dir = str(getenv('HUMMINGBOT_REPO_DIR'))
    if hummingbot_repo_dir in (None, ""):
        raise ValueError("{HUMMINGBOT_REPO_DIR} environmental variable not set")
    gen_dir = path.abspath(strategy_gen_dir)

    dest_strategy_dir = path.join(hummingbot_repo_dir, 'hummingbot',
                                  'strategy', f'{strategy_name}')
    dest_template_dir = path.join(hummingbot_repo_dir, 'hummingbot',
                                  'templates')
    if not path.isdir(dest_strategy_dir):
        mkdir(dest_strategy_dir)

    for file in listdir(gen_dir):
        if file.split('.')[1] == 'py':
            shutil.copyfile(
                path.join(gen_dir, file), path.join(dest_strategy_dir, file)
            )
        elif file.split('.')[1] == 'yml':
            shutil.copyfile(
                path.join(gen_dir, file), path.join(dest_template_dir, file)
            )
    print(f'Execute: cd {hummingbot_repo_dir} && conda activate hummingbot && ./compile')


def main():
    cli(obj={})
