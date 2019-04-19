"""
https://open.kattis.com/problems/coast
A program to find the total length of a coastline given the coordinates of islands.
"""


# Starting the the top-left corner of our 2D array (guaranteed to be a sea tile thanks to the 'border' we've built),
# we check each horizontal and vertical neighbor of the current tile
def iterate_sea_tiles(map_array):
    unvisited_sea_coordinates = {(0, 0)}
    total_sea_coast_count = 0
    # We use offsets to avoid index out of bounds errors
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Iterate through our set of unvisited sea tiles until it is empty (i.e., we've visited every sea tile)
    while unvisited_sea_coordinates:

        # Pop an arbitrary coordinate tuple from our set, and change that coordinate's value on the 2D array to '2'
        # (To represent it having been visited already)
        y_position, x_position = unvisited_sea_coordinates.pop()
        map_array[y_position][x_position] = 2
        for offset in offsets:
            target_location = (y_position + offset[0], x_position + offset[1])

            # If the index would put us out of bounds, do not try to visit that location, and skip to the next
            # neighbor
            if not 0 <= target_location[0] < len(map_array) or not 0 <= target_location[1] < len(map_array[0]):
                continue
            else:
                # If the neighbor is a 0, we add it to the list of unvisited sea tiles
                if map_array[target_location[0]][target_location[1]] == 0 \
                        and (target_location[0], target_location[1]) not in unvisited_sea_coordinates:
                    unvisited_sea_coordinates.add((target_location[0], target_location[1]))
                # If the neighbor is a 1, we increment our total sea coastline by 1
                elif map_array[target_location[0]][target_location[1]] == 1:
                    total_sea_coast_count += 1
    return total_sea_coast_count


# Take in user input, and split it into two variables: Amount of arrays given, and length of each array given
initial_input = input()
initial_input_list = initial_input.split(' ')

# We add two to each of these variables to build an extra 'border' of sea around the given map
amount_of_lists_given = int(initial_input_list[0]) + 2
length_of_lists_given = int(initial_input_list[1]) + 2

map_2D_array = [[0] * length_of_lists_given]
for listCount in range(1, amount_of_lists_given - 1):
    current_array_input = input()
    # We build a new row with 0 as its first and last elements (to build a 'border' of sea around the list), and
    # build the next row of our 2D array with the information passed to us
    current_array_row = [0]
    current_array_row.extend(list(current_array_input))
    current_array_row = [int(current_index) for current_index in current_array_row]
    current_array_row.append(0)
    # We then append this row to our 2D array
    map_2D_array.append(current_array_row)
map_2D_array.append([0] * length_of_lists_given)

print(iterate_sea_tiles(map_2D_array))
