def get_subset(data: list[dict], node_nums: list[int]) -> list[dict]:
    node_num_subset = set(node_nums)
    output = []
    for ds in data:
        output.append(_get_subset_ds(ds, node_num_subset))
    return output


def _get_subset_ds(ds: dict, node_num_subset: set[int]):
    if ds["type"] == 15:
        return _reduce_dataset(
            ds, node_num_subset, ["def_cs", "disp_cs", "color", "x", "y", "z"]
        )
    elif ds["type"] == 55:
        return _reduce_dataset(
            ds, node_num_subset, ["r1", "r2", "r3"], ["r4", "r5", "r6"]
        )
    else:
        raise ValueError(f"Unknown dataset type ({ds['type']})")


def _reduce_dataset(
    ds: dict,
    node_num_subset: set[int],
    required_fields: list[str],
    optional_fields: list[str] = None,
) -> dict:
    ds = ds.copy()
    idx = [i for i, n in (enumerate(ds["node_nums"])) if n in node_num_subset]
    ds["node_nums"] = _get_subset_by_idx(ds["node_nums"], idx)
    for field in required_fields:
        ds[field] = _get_subset_by_idx(ds[field], idx)
    if optional_fields:
        for field in optional_fields:
            try:
                ds[field] = _get_subset_by_idx(ds[field], idx)
            except KeyError:
                ...
    return ds


def _get_subset_by_idx(data: list, idx: list[int]) -> list:
    return [data[i] for i in idx]
