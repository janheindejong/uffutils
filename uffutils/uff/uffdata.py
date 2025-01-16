from __future__ import annotations

from typing import Generator

from uffutils.uff.dataset import Dataset
from uffutils.uff.subsetmap import SubsetMap


class UFFData:
    """
    Represents UFFData from a file. Couple of limitations / assumptions:
    - Assumes exactly one UFF15 dataset to be present
    - Currently only understands UFF15, 18 and 55

    It requires data in the structure specified by our friends from PyUFF,
    making it play nicely with that.
    """

    _datasets: list[Dataset]

    def __init__(self, datasets: list[dict]):
        self._datasets = []
        for ds in datasets:
            self._datasets.append(Dataset(ds))
        self._validate()

    def __len__(self):
        return self._datasets.__len__()

    def get_set_types(self) -> list[int]:
        return [ds.type for ds in self._datasets]

    def get_set_type_count(self) -> dict:
        d: dict = {}
        for t in self.get_set_types():
            if t in d:
                d[t] += 1
            else:
                d[t] = 1
        return d

    def get_nodes(self) -> list[int]:
        return self._get_uff_15().node_nums

    def subset(
        self,
        target_nodes: list[int] | None = None,
        step: int | None = None,
        n_max: int | None = None,
    ):
        if not target_nodes:
            target_nodes = self.get_nodes()
        if step:
            target_nodes = target_nodes[::step]
        if n_max:
            target_nodes = target_nodes[:n_max]
        for ds in self._datasets:
            ds.accept(SubsetMap(target_nodes))

    def scale(self, length=1) -> None: ...

    def rotate(self, r_x, r_y, r_z) -> None: ...

    def translate(self, x, y, z) -> None: ...

    def cs_to_global(self) -> None: ...

    def export(self) -> Generator[dict]:
        for ds in self._datasets:
            yield ds._export()

    def _validate(self) -> None:
        # Check UFF15 constraint
        if self.get_set_types().count(15) != 1:
            raise Exception("Should have exactly one UFF15 dataset.")

    def _get_uff_15(self) -> Dataset:
        for ds in self._datasets:
            if ds.type == 15:
                return ds
        raise Exception("Can't find UFF15.")
