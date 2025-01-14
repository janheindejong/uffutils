def get_nodes(ds: dict, step: int = 1) -> list[int]:
    return list(map(int, ds["node_nums"][::step]))
