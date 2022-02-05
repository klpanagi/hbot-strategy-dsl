import sys
import os
from os import path, getenv, mkdir, listdir
import shutil
import click
import subprocess

from .generator import generate as hbot_generator


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
    # hbot_strategy_model_validator(model_path)

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
    # os.system(
    #     f'conda activate hummingbot && cd {hummingbot_repo_dir} && ./compile'
    # )
    # proc = subprocess.Popen(
    #     [f"conda init zsh && conda activate hummingbot && cd {hummingbot_repo_dir} && ./compile"],
    #     shell=True,
    #     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )
    # output, err = proc.communicate()
    # print(output)
    # print(err)
    print(f'Execute: cd {hummingbot_repo_dir} && conda activate hummingbot && ./compile')


def main():
    cli(obj={})
