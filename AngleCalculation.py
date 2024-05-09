import numpy as np
import math


# Calculate the Sensor Sway Angle for the current time
def calculate_angle(node_num, data):

    # Get quaternions
    qw = data[node_num]["Quat1"]
    qx = data[node_num]["Quat2"]
    qy = data[node_num]["Quat3"]
    qz = data[node_num]["Quat4"]

    # Convert quaternions to Euler angles
    # bediyap.com/programming/convert-quaternion-to-euler-rotations/

    # case zyz, Rotation sequence: Z->Y->Z
    t0 = 2 * (qy * qz + qw * qx)
    t1 = -2 * (qx * qz - qw * qy)

    roll = np.arctan2(t0, t1)  # in radians
    roll = roll*180/3.14159 + 90  # in deg and adjusted for keeping the sensor vertical

    # this_angle is corresponding to the sway angle when the sensor is kept vertical with switch pointing up
    this_angle = roll

    return this_angle
