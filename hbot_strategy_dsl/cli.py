import sys
import click

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


def main():
    cli(obj={})
