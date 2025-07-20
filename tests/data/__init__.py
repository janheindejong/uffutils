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
    }
}
