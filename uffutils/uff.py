from __future__ import annotations

from typing import Generator, Iterable


class UFFData:
    """
    Represents UFFData from a file. Couple of limitations / assumptions:
    - Assumes exactly one UFF15 dataset to be present
    - Currently only understands UFF15, 18 and 55

    It requires data in the structure specified by our friends from PyUFF,
    making it play nicely with that.
    """

    _datasets: list[DatasetBase]

    def __init__(self, datasets: list[dict]):
        self._datasets = []
        for ds in datasets:
            if ds["type"] == 15:
                self._datasets.append(UFF15(ds))
            elif ds["type"] == 55:
                self._datasets.append(UFF55(ds))
            else:
                self._datasets.append(DatasetBase(ds))
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
    
    def subset(self, target_nodes: list[int] | None = None, step: int | None = None, n_max: int | None = None):
        if not target_nodes: 
            target_nodes = self.get_nodes()
        if step: 
            target_nodes = target_nodes[::step]
        if n_max: 
            target_nodes = target_nodes[:n_max]
        for ds in self._datasets:
            ds.subset(target_nodes)

    def scale(self, length=1) -> None: ...

    def rotate(self, r_x, r_y, r_z) -> None: ...

    def translate(self, x, y, z) -> None: ...

    def cs_to_global(self) -> None: ...

    def export(self) -> Generator[dict]:
        for ds in self._datasets:
            yield ds.export()

    def _validate(self) -> None:
        # Check UFF15 constraint
        if self.get_set_types().count(15) != 1:
            raise Exception("Should have exactly one UFF15 dataset")

    def _get_uff_15(self) -> UFF15:
        for ds in self._datasets:
            if isinstance(ds, UFF15):
                return ds
        raise Exception("Can't find UFF15")


class DatasetBase:
    _ds: dict
    _subset_strategy: SubsetStrategy

    def __init__(self, ds: dict):
        self._ds = ds
        self._subset_strategy = SubsetStrategy([])

    @property
    def type(self) -> int:
        return self._ds["type"]

    @property
    def node_nums(self) -> list[int]:
        return list(map(int, self._ds["node_nums"]))

    def subset(self, target_nodes: Iterable[int]) -> None:
        self._subset_strategy.subset(self._ds, target_nodes)

    def export(self) -> dict:
        return self._ds


class UFF15(DatasetBase):
    def __init__(self, ds):
        super().__init__(ds)
        self._subset_strategy = SubsetStrategy(
            ["def_cs", "disp_cs", "color", "x", "y", "z"]
        )


class UFF55(DatasetBase):
    def __init__(self, ds):
        super().__init__(ds)
        self._subset_strategy = SubsetStrategy(["r1", "r2", "r3"], ["r4", "r5", "r6"])


class SubsetStrategy:
    def __init__(
        self, required_fields: list[int], optional_fields: list[int] | None = None
    ):
        self._required_fields = required_fields
        self._optional_fields = optional_fields

    def subset(self, ds: dict, target_nodes: Iterable[int]) -> None:
        # Ideally, users send this stuff as a set, but for convenience we check it here.
        if not isinstance(target_nodes, set):
            target_nodes = set(target_nodes)

        # Get indices of target nodes
        idx = [i for i, n in (enumerate(ds["node_nums"])) if n in target_nodes]

        # Reduce node nums
        ds["node_nums"] = self._get_subset_by_idx(ds["node_nums"], idx)

        # Reduce all other fields
        for field in self._required_fields:
            ds[field] = self._get_subset_by_idx(ds[field], idx)
        if self._optional_fields:
            for field in self._optional_fields:
                try:
                    ds[field] = self._get_subset_by_idx(ds[field], idx)
                except KeyError:
                    # If an optional field is not find, no biggie (e.g., complex values)
                    ...

    @staticmethod
    def _get_subset_by_idx(data: list, idx: list[int]) -> list:
        return [data[i] for i in idx]
