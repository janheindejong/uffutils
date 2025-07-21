from typing import Any, Iterable


class SubsetMap:
    def __init__(
        self,
        nodes: Iterable[int],
        target_nodes: Iterable[int],
        fields: list[str],
    ):
        if not isinstance(target_nodes, set):
            target_nodes = set(target_nodes)
        else:
            target_nodes = target_nodes

        self._idx = [i for i, n in (enumerate(nodes)) if n in target_nodes]
        self.fields = fields

    def apply(self, ds: dict[str, Any]) -> None:
        for k in self.fields:
            ds[k] = self._get_subset_by_idx(ds[k], self._idx)

    @staticmethod
    def _get_subset_by_idx(data: list, idx: list[int]) -> list:
        return [data[i] for i in idx]
