import numpy as np


class RotateMap: 

    def __init__(self, angles: tuple[float, float, float], fields: tuple[str, str, str]) -> None:
        self._angles = angles
        self._fields = fields

    def apply(self, ds: dict) -> None: 
        X = np.array([ds[field] for field in self._fields])
        X = self._rot_mat(*self._angles) @ X
        for i, field in enumerate(self._fields): 
            ds[field] = X[i]

    def _rot_mat(self, roll, pitch, yaw) -> np.ndarray: 
        c = lambda x: np.cos(x)
        s = lambda x: np.sin(x)
        Rx = np.array([
            [1, 0 , 0],
            [0, c(roll), -s(roll)],
            [0, s(roll), c(roll)]
        ])
        Ry = np.array([
            [c(pitch), 0, s(pitch)], 
            [0, 1, 0], 
            [-s(pitch), 0, c(pitch)]
        ])
        Rz = np.array([
            [c(yaw), -s(yaw), 0], 
            [s(yaw), c(yaw), 0], 
            [0, 0, 1]
        ])
        return Rz @ Ry @ Rx
        