import pytest

from uffutils import get_nodes, get_subset, read

_test_file_large = "tests\\data\\large.uff"
_test_file_small = "tests\\data\\small.uff"


@pytest.mark.parametrize(
    "path,n_nodes,sets",
    [(_test_file_large, 21521, [15] + [55] * 50), (_test_file_small, 3, [15, 55])],
)
def test_read(path: str, n_nodes: int, sets: list[int]):
    data = read(path)
    assert len(data) == len(sets)
    assert [ds["type"] for ds in data] == sets
    assert len(data[0]["node_nums"]) == n_nodes


@pytest.mark.parametrize(
    "path,step,n_nodes,first",
    [
        (_test_file_large, 1, 21521, [101, 102, 103]),
        (_test_file_small, 1, 3, [101, 102, 103]),
    ],
)
def test_nodes(path: str, step: int, n_nodes: int, first: list[int]):
    data = read(path)
    nodes = get_nodes(data[0], step)
    assert len(nodes) == n_nodes
    assert nodes[:3] == first


@pytest.mark.parametrize("path,node_subset", [(_test_file_small, [101, 103])])
def test_subset(path: str, node_subset: list[int]):
    data = read(path)
    data = get_subset(data, node_subset)
    assert data[0]["node_nums"] == [101, 103]
    assert data[1]["node_nums"] == [101, 103]
    assert len(data[1]["r1"]) == 2
