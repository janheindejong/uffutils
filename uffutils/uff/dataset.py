from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Protocol, runtime_checkable

from uffutils.uff.rotatemap import RotateMap
from uffutils.uff.subsetmap import SubsetMap


class Dataset:
    _ds: dict

    def __init__(self, ds: dict):
        self._ds = ds

    @property
    def type(self) -> int:
        return self._ds["type"]

    def export(self) -> dict:
        return self._ds


@runtime_checkable
class ISubsetable(Protocol):
    @abstractmethod
    def subset(self, target_nodes: Iterable[int]) -> None: ...


@runtime_checkable
class IScaleable(Protocol):
    @abstractmethod
    def scale(self, length: float | int) -> None: ...


@runtime_checkable
class ITranslatable(Protocol):
    @abstractmethod
    def translate(self, x: float, y: float, z: float) -> None: ...


@runtime_checkable
class IRotatable(Protocol):
    @abstractmethod
    def rotate(self, angles: tuple[float, float, float]) -> None: ...


class UFF15Dataset(Dataset, ISubsetable, IScaleable, ITranslatable, IRotatable):
    @property
    def node_nums(self) -> list[int]:
        return list(map(int, self._ds["node_nums"]))

    def subset(self, target_nodes: Iterable[int]):
        subset_map = SubsetMap(
            self.node_nums,
            target_nodes,
            ["node_nums", "def_cs", "disp_cs", "color", "x", "y", "z"],
        )
        subset_map.apply(self._ds)

    def scale(self, length: float | int) -> None:
        for d in "xyz":
            self._ds[d] = [pos * length for pos in self._ds[d]]

    def translate(self, x: float, y: float, z: float) -> None:
        for translation, d in zip((x, y, z), "xyz", strict=False):
            self._ds[d] = [pos + translation for pos in self._ds[d]]

    def rotate(self, angles: tuple[float, float, float]) -> None:
        rotate_map = RotateMap(angles, ("x", "y", "z"))
        rotate_map.apply(self._ds)


class UFF55Dataset(Dataset, ISubsetable, IRotatable):
    @property
    def has_rotations(self) -> bool:
        return self._ds["data_ch"] == 3

    def subset(self, target_nodes: Iterable[int]):
        fields = ["node_nums", "r1", "r2", "r3"]
        if self.has_rotations:
            fields += ["r4", "r5", "r6"]
        subset_map = SubsetMap(
            self._ds["node_nums"],
            target_nodes,
            fields,
        )
        subset_map.apply(self._ds)

    def rotate(self, angles: tuple[float, float, float]) -> None:
        rotate_maps = [RotateMap(angles, ("r1", "r2", "r3"))]
        if self.has_rotations:
            rotate_maps.append(RotateMap(angles, ("r4", "r5", "r6")))
        for rmap in rotate_maps:
            rmap.apply(self._ds)
