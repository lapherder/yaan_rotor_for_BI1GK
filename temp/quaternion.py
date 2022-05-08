from math import *


def ToQuaternion(yaw,pitch,roll):
    cy = cos(yaw * 0.5)
    sy = sin(yaw * 0.5)
    cp = cos(pitch * 0.5)
    sp = sin(pitch * 0.5)
    cr = cos(roll * 0.5)
    sr = sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    i = sr * cp * cy - cr * sp * sy
    j = cr * sp * cy + sr * cp * sy
    k = cr * cp * sy - sr * sp * cy

    return (w,i,j,k)

print(ToQuaternion(20,85,0))
print(ToQuaternion(20,86,0))
print(ToQuaternion(20,97,0))
print(ToQuaternion(20,88,0))