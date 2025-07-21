import numpy as np
from scipy.spatial.transform import Rotation

roll, pitch, yaw  = angles = np.pi / 2, np.pi / 2, np.pi / 2 


def rotmat(roll, pitch, yaw):
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


def rotmat_scipy(roll, pitch, yaw): 
    return Rotation.from_euler("ZYX", [yaw, pitch, roll]).as_matrix()


def rotmat_extrinsic_scipy(roll, pitch, yaw): 
    return Rotation.from_euler("xyz", [roll, pitch, yaw]).as_matrix()


R1 = rotmat(*angles).round(2)
R2 = rotmat_scipy(*angles).round(2)
R4 = rotmat_extrinsic_scipy(*angles).round(2)

assert (R1 == R2).all()
assert (R1 == R4).all()

x = R1 @ np.array([1, 0, 0])

print(x)
