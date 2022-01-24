import os
from textx import language, metamodel_from_file
import pathlib

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()


def get_metamodel():
    metamodel = metamodel_from_file(
        CURRENT_FPATH.joinpath('grammar/strategy.tx'),
        classes=[]
    )
    return metamodel


def build_model(model_path):
    # Parse model
    model = get_metamodel().model_from_file(model_path)
    return model


@language('hummingbot', '*.strategy')
def _language():
    "Hummingbot Strategy DSL"
    return get_metamodel()
