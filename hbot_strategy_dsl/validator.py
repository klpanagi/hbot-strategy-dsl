import os
import pathlib

from .language import build_model

CURRENT_FPATH = pathlib.Path(__file__).parent.resolve()


def validate_from_file(model_fpath) -> bool:
    try:
        model = build_model(model_fpath)
    except Exception as e:
        print(e)
        return False
    else:
        print(f'Validation of model (file={model_fpath}) passed!')

