"""
https://open.kattis.com/problems/logo2
A program to find a missing movement or rotation given a list of those commands with a shared startpoint and endpoint.
"""

import math


# Takes in two sets of coordinates (A and B) and returns the vectors from the origin to B, and from B to A
def vector_maker(stored_coordinates, end_coordinates):
    origin_to_stored_coords_vector = (stored_coordinates[0], stored_coordinates[1])
    stored_to_end_coords_vector = (end_coordinates[0] - stored_coordinates[0],
                                   end_coordinates[1] - stored_coordinates[1])
    return origin_to_stored_coords_vector, stored_to_end_coords_vector


# Find the absolute distance between our starting point and our current endpoint
def get_missing_distance(x, y):
    missing_value = math.hypot(x, y)
    return round(missing_value)


# Find the missing angle, using the dot product and determinant of the vectors from the origin to the stored
# coordinates, and from the stored coordinates to the endpoint
# Uses atan2 to ensure that the angle returned is accurate to 360 degrees, and not just to 180 degrees
def get_missing_degree(recent_coordinates, stored_coordinates):
    vec1, vec2 = vector_maker(stored_coordinates, recent_coordinates)
    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
    determinant = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    inner_angle = math.degrees(math.atan2(determinant, dot_product)) + 180
    return (round(inner_angle)) % 360


# Adjust the x and y coordinates based on the given r value and theta
def apply_movement(r_value, theta, x_coordinate, y_coordinate):
    x_coordinate += r_value * math.cos(math.radians(theta))
    y_coordinate += r_value * math.sin(math.radians(theta))
    return x_coordinate, y_coordinate


# Adjust the total theta value by the given theta, mod 360
def apply_rotation(current_theta, total_theta):
    total_theta += current_theta
    total_theta %= 360
    return total_theta


number_of_test_cases = input()
for test_case in range(int(number_of_test_cases)):
    x_value = 0
    y_value = 0
    theta = 0
    command_to_check = ''

    # Used to find the missing angle of the polygon, if one exists
    stored_coordinates = (0, 0)

    number_of_commands = input()
    for command in range(int(number_of_commands)):
        current_command = input()
        order, unit = current_command.split(' ')
        # If the unit is our unknown, store the order to solve later
        if unit == "?":
            command_to_check = order
            # If our unknown is a rotation command, store our current x and y coordinates to solve for the missing
            # angle later
            if order == "lt" or order == "rt":
                stored_coordinates = (x_value, y_value)

        else:
            unit = int(unit)
            # If the order is a movement command, update our x and y coordinates based on the polar coordinate system
            if order == "fd":
                x_value, y_value = apply_movement(unit, theta, x_value, y_value)
            elif order == "bk":
                x_value, y_value = apply_movement(-unit, theta, x_value, y_value)

            # If the order is a rotation command, update our theta angle
            elif order == "lt":
                theta = apply_rotation(unit, theta)
            elif order == "rt":
                theta = apply_rotation(-unit, theta)

    # If we are looking for a movement command, simply find the distance between our final location and the origin
    if command_to_check == "fd" or command_to_check == "bk":
        print(get_missing_distance(x_value, y_value))

    # If we are looking for a rotation command, we must find the angle between the vector from the origin to the stored
    # coordinates, and the vector from the stored coordinates to our ending coordinates
    # Since we always find the counterclockwise angle with the function above, and a left turn requires a clockwise
    # angle, we must subtract our answer from 360 if we're making a left turn
    elif command_to_check == "lt":
        final_angle = get_missing_degree((x_value, y_value), stored_coordinates)
        print((360 - final_angle) % 360)
    else:
        print(get_missing_degree((x_value, y_value), stored_coordinates))
