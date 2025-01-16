from typing import Iterable

from uffutils.uff.dataset import Dataset, IDatasetVisitor


class SubsetMap(IDatasetVisitor):
    def __init__(self, target_nodes: Iterable[int]):
        if not isinstance(target_nodes, set):
            self._target_nodes = set(target_nodes)
        else:
            self._target_nodes = target_nodes

    def apply(self, dataset: Dataset) -> None:
        if dataset.type == 15:
            self._apply(dataset._ds, ["def_cs", "disp_cs", "color", "x", "y", "z"])
        elif dataset.type == 55:
            self._apply(dataset._ds, ["r1", "r2", "r3"], ["r4", "r5", "r6"])
        else:
            raise NotImplementedError(
                f"Applying a subset over UFF{dataset.type} is not supported."
            )

    def _apply(
        self,
        ds: dict,
        required_fields: list[str],
        optional_fields: list[str] | None = None,
    ) -> None:
        # Get indices of target nodes
        idx = [i for i, n in (enumerate(ds["node_nums"])) if n in self._target_nodes]

        # Reduce node nums
        ds["node_nums"] = self._get_subset_by_idx(ds["node_nums"], idx)

        # Reduce all other fields
        for field in required_fields:
            ds[field] = self._get_subset_by_idx(ds[field], idx)
        if optional_fields:
            for field in optional_fields:
                try:
                    ds[field] = self._get_subset_by_idx(ds[field], idx)
                except KeyError:
                    # No biggie if optional fields not found (e.g., complex values)
                    ...

    @staticmethod
    def _get_subset_by_idx(data: list, idx: list[int]) -> list:
        return [data[i] for i in idx]
