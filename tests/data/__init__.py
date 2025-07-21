from pathlib import Path


datasets = {
    "large": {
        "path": Path("tests/data/large.uff"),
        "properties": {
            "n_sets": 51,
            "sets": [15] + [55] * 50,
            "n_nodes": 21521,
            "first_node_nums": [101, 102, 103],
        },
    },
    "subset": {
        "path": Path("tests/data/subset.uff"),
        "properties": {
            "n_sets": 51,
            "sets": [15] + [55] * 50,
            "n_nodes": 100,
            "first_node_nums": [101, 11018075, 11051008],
        },
    },
    "subset_rotated": {
        "path": Path("tests/data/subset_rotated.uff"),
        "properties": {
            "n_sets": 51,
            "sets": [15] + [55] * 50,
            "n_nodes": 100,
            "first_node_nums": [101, 11018075, 11051008],
        },
    },
}
