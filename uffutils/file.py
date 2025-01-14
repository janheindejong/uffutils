import json
import os

import pyuff
import numpy as np


def read(path: str) -> list[dict]:
    path = os.path.abspath(path)
    uff = pyuff.UFF(path)
    data = uff.read_sets()
    for ds in data:
        _ndarray_to_list_in_place(ds)
    return data


def write(path: str, datasets: dict, overwrite: bool = True) -> str:
    path = os.path.abspath(path)
    uff = pyuff.UFF(path)
    if overwrite:
        mode = "overwrite"
    else:
        mode = "add"
    uff.write_sets(datasets, mode)
    return path


def deserialize(data: str) -> list[dict]:
    return json.loads(data)


def serialize(data: list[dict]):
    return json.dumps(data)


def _ndarray_to_list_in_place(data: dict) -> None:
    for key, value in data.items():
        if isinstance(value, np.ndarray):
            data[key] = list(value)
