from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

@dataclass
class DatasetProperties:
    n_sets: int
    sets: List[int]
    n_nodes: int
    first_node_nums: List[int]

@dataclass
class Dataset:
    path: Path
    properties: DatasetProperties

datasets: Dict[str, Dataset] = {
    "large": Dataset(
        path=Path("tests/data/large.uff"),
        properties=DatasetProperties(
            n_sets=51,
            sets=[15] + [55] * 50,
            n_nodes=21521,
            first_node_nums=[101, 102, 103],
        )
    ),
    "subset": Dataset(
        path=Path("tests/data/subset.uff"),
        properties=DatasetProperties(
            n_sets=51,
            sets=[15] + [55] * 50,
            n_nodes=100,
            first_node_nums=[101, 11018075, 11051008],
        )
    ),
    "subset_rotated": Dataset(
        path=Path("tests/data/subset_rotated.uff"),
        properties=DatasetProperties(
            n_sets=51,
            sets=[15] + [55] * 50,
            n_nodes=100,
            first_node_nums=[101, 11018075, 11051008],
        )
    ),
}