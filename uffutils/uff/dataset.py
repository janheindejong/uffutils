from __future__ import annotations

from typing import Protocol


class IDatasetVisitor(Protocol):
    def apply(self, dataset: Dataset): ...


class Dataset:
    _ds: dict

    def __init__(self, ds: dict):
        self._ds = ds

    @property
    def type(self) -> int:
        return self._ds["type"]

    @property
    def node_nums(self) -> list[int]:
        return list(map(int, self._ds["node_nums"]))

    def accept(self, visitor: IDatasetVisitor):
        visitor.apply(self)

    def _export(self) -> dict:
        return self._ds
