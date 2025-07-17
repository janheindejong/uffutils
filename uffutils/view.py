from collections import Counter
from typing import Protocol
from uffutils.uff.dataset import Dataset
from uffutils.uff.uffdata import UFFData


class Viewer(Protocol):

    def print_full(self) -> str: ...

    def print_summary(self) -> str: ...


class UFFDataViewer(Viewer): 

    def __init__(self, data: UFFData):
        self._sets_viewer = SetsViewer(data._datasets)


class NodesViewer(Viewer):

    def __init__(self, node_nums: list[int]):
        self._node_nums = node_nums

    def print_full(self) -> str:
        return ", ".join(self._node_nums)

    def print_summary(self) -> str:
        return 


        


class SetsViewer(Viewer):

    def __init__(self, sets: list[Dataset]):
        self._sets = sets

    def print_full(self):
        return ", ".join(self._set_types())

    def print_summary(self):
        s = "Sets:\n"
        s += f"  Count: {len(self._sets)}\n"
        s += "  Type count: " + self._set_count_str() + "\n"
        s += "  Types: " + self._set_types_str()
        return s

    def _set_types_str(self):
        t = self._set_types()
        if len(t) > 5:
            return ", ".join(t[:2]) + ", ..., " + ", ".join(t[-2:])
        else:
            return ", ".join(t)

    def _set_types(self) -> list:
        return [d.type for d in self._sets]

    def _set_count_str(self) -> dict:
        c = []
        for k, v in self._set_count():
            c += f"{k} ({v})"
        return ", ".join(c)

    def _set_count(self) -> dict:
        return dict(Counter(self._set_types))
