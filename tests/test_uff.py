import math

import numpy as np
import pytest

from uffutils import UFFData, read

from .data import datasets

test_data = datasets["large"]


@pytest.fixture
def dataset() -> UFFData:
    return read(str(test_data.path))


def test_sets(dataset: UFFData):
    assert len(dataset) == test_data.properties.n_sets
    assert dataset.get_set_types() == test_data.properties.sets


def test_nodes(dataset: UFFData):
    nodes = dataset.get_nodes()
    assert len(nodes) == test_data.properties.n_nodes
    assert nodes[:3] == test_data.properties.first_node_nums


def test_subset_step(dataset: UFFData):
    dataset.subset(step=2)
    nodes = dataset.get_nodes()
    data = list(dataset.export())

    expected_nodes = test_data.properties.first_node_nums[::2]
    expected_n_nodes = math.ceil(test_data.properties.n_nodes / 2)

    # Verify if UFF15 is handled correctly
    assert nodes[:2] == expected_nodes
    assert len(nodes) == expected_n_nodes

    # Verify if UFF55 sets are handled correctly
    assert len(data[1]["node_nums"]) == expected_n_nodes
    assert list(map(int, data[1]["node_nums"]))[:2] == expected_nodes
    assert len(data[1]["r1"]) == expected_n_nodes
    assert data[1]["r1"][1] == 0.23208


def test_subset_list(dataset: UFFData):
    dataset.subset(target_nodes=[101, 103])
    nodes = dataset.get_nodes()
    data = list(dataset.export())

    # Verify if UFF15 is handled correctly
    assert nodes[:2] == [101, 103]
    assert len(nodes) == 2

    # Verify if UFF55 sets are handled correctly
    assert len(data[1]["node_nums"]) == 2
    assert data[1]["node_nums"][1] == 103
    assert len(data[1]["r1"]) == 2
    assert data[1]["r1"][1] == 0.23208


def test_subset_max(dataset: UFFData):
    dataset.subset(n_max=3)
    nodes = dataset.get_nodes()
    data = list(dataset.export())

    # Verify if UFF15 is handled correctly
    assert nodes == test_data.properties.first_node_nums
    assert len(nodes) == 3

    # Verify if UFF55 sets are handled correctly
    assert len(data[1]["node_nums"]) == 3
    assert list(map(int, data[1]["node_nums"])) == test_data.properties.first_node_nums
    assert len(data[1]["r1"]) == 3
    assert data[1]["r1"][2] == 0.23208


def test_scale(dataset: UFFData):
    dataset.subset(n_max=3)
    dataset.scale(length=10)
    data = list(dataset.export())

    # Verify UFF15 is scaled correctly
    assert data[0]["x"] == pytest.approx([1198.5, 1198.5, 1198.5])
    assert data[0]["y"] == pytest.approx([64.38, 392.46, 720.55])
    assert data[0]["z"] == pytest.approx([126.82, 126.82, 126.82])


def test_translate(dataset: UFFData):
    dataset.subset(n_max=3)
    dataset.translate(1, 2, 3)
    data = list(dataset.export())

    # Verify UFF15 is translated correctly
    assert data[0]["x"] == pytest.approx([120.85, 120.85, 120.85])
    assert data[0]["y"] == pytest.approx([8.437999, 41.246, 74.055])
    assert data[0]["z"] == pytest.approx([15.682, 15.682, 15.682])


def test_rotate(dataset: UFFData):
    dataset.subset(n_max=3)
    dataset.rotate((np.pi / 2, np.pi / 2, np.pi / 2))
    data = list(dataset.export())

    assert data[0]["x"] == pytest.approx([12.682, 12.682, 12.682])
    assert data[0]["y"] == pytest.approx([6.438, 39.246, 72.055])
    assert data[0]["z"] == pytest.approx([-119.85, -119.85, -119.85])

    assert data[1]["r1"] == pytest.approx([0.14233, 0.13904, 0.13576])
    assert data[1]["r2"] == pytest.approx([-0.37665, -0.37665, -0.37665])
    assert data[1]["r3"] == pytest.approx([0.11726, -0.057409, -0.23208])
