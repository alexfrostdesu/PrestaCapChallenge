from typing import List, Tuple, Set, Iterable
import numpy as np
import itertools


class GridError(Exception):
    pass


def input_grid(grid: list = None) -> list:
    """
    Inputting grid and splitting it to list of strings
    :param grid: (optional) predefined grid
    :return: grid
    """
    if grid is None:
        print("Please enter grid as strings, divided by commas")
        in_grid = input("Grid: ")
        processed_grid = in_grid.replace(' ', '').split(',')
        return processed_grid
    else:
        return grid


def input_grid_size(n: int = None) -> int:
    """
    Inputting grid size and checking if it is valid
    :param n: (optional) predefined grid size
    :return: grid size
    """
    if n is None:
        print("Please enter grid size as integer")
        in_size = input("Grid size: ")
        try:
            processed_size = int(in_size)
            if processed_size <= 0:
                raise GridError("Incorrect grid size, should be more than 0")
            return processed_size
        except ValueError:
            print("Not a correct integer number")
    else:
        return n


def parse_grid(grid: List[str], grid_size: int) -> Tuple[tuple, tuple, np.ndarray]:
    """
    Validating the inputted grid and returning the positions of Mario and princess, along with grid in array format
    :param grid_size: size of the grid (size*size)
    :param grid: inputted grid as list of strings
    :return: Mario and princess positions in tuple format and validated grid in numpy array format
    """
    # checking if the grid is the correct size (N)
    if len(grid) != grid_size:
        raise GridError("Incorrect grid size")

    # list of correct signs in the grid
    acceptable_signs = ['-', 'm', 'p', 'x']
    # initializing variables for Mario and princess
    mario_position = None
    princess_position = None

    for line_num, line in enumerate(grid):
        # type check
        if type(line) is not str:
            raise GridError("Line {} is not defined by string".format(line_num))
        # line (row) size check
        elif len(line) != grid_size:
            raise GridError("Incorrect line {} size".format(line_num))

        for elem_num, elem in enumerate(line):
            # checking if every sign in the strings is acceptable
            if elem not in acceptable_signs:
                raise GridError("Incorrect sign on line {}, position {}".format(line_num, elem_num))
            # getting princess position
            elif elem == 'p':
                if princess_position is None:
                    princess_position = (line_num, elem_num)
                else:
                    raise GridError("Multiple princess positions defined")
            # getting Mario position
            elif elem == 'm':
                if mario_position is None:
                    mario_position = (line_num, elem_num)
                else:
                    raise GridError("Multiple Mario positions defined")

    # check if Mario and princess were found on the grid
    if mario_position is None:
        raise GridError("Mario position is not defined")
    if mario_position is None:
        raise GridError("Princess position is not defined")

    # converting grid to usable array form
    grid_array = np.array([list(line) for line in grid])

    return mario_position, princess_position, grid_array


def get_easy_possible_paths(mario_position: tuple, princess_position: tuple) -> Set[tuple]:
    """
    Getting all possible 'easy' paths made from coordinates difference between Mario and princess
    :param mario_position: Mario position
    :param princess_position: princess position
    :return: set of all possible paths
    """
    # getting 'distance' between Mario and princess in coordinates
    distance = np.subtract(princess_position, mario_position)

    # create required moves from distance
    moves_list = []
    for i in range(abs(distance[0])):
        moves_list.append((1, 0) if distance[0] >= 0 else (-1, 0))
    for i in range(abs(distance[1])):
        moves_list.append((0, 1) if distance[1] >= 0 else (0, -1))

    # create possible paths from possible moves, using set to remove duplicates
    all_paths_list = set(itertools.permutations(moves_list))
    return all_paths_list


def find_working_paths(paths: Iterable[tuple], starting_position: tuple, grid: np.ndarray) -> List[tuple]:
    """
    Checking possible paths for running into obstacles
    :param paths: iterable of possible paths
    :param starting_position: starting position
    :param grid: validated array of a grid
    :return: list of all working paths
    """
    moves_dict = {(1, 0): "DOWN", (-1, 0): "UP", (0, 1): "RIGHT", (0, -1): "LEFT"}
    successful_paths = []
    for path in paths:
        # starting from starting position
        new_pos = starting_position
        path_check = []
        for move in path:
            # moving to new position and checking if it is valid
            new_pos = tuple(np.add(new_pos, move))
            path_check.append(True if grid[new_pos] != 'x' else False)

        # if all moves are valid, adding path to success list
        if all(path_check):
            successful_paths.append(tuple(moves_dict[move] for move in path))

    return successful_paths


def check_valid_move(grid: np.ndarray, current_position: tuple, move: tuple) -> bool:
    """
    Checking if move is valid for the current position in provided grid
    :param grid: validated array of a grid
    :param current_position: current position
    :param move: move in tuple form
    :return: True or False
    """
    # getting coordinates for moved position
    moved_position = tuple(np.add(current_position, move))

    def compare_coordinates(a: tuple, b: tuple) -> bool:
        """
        Helper function to compare coordinates
        Checks if a is smaller than b
        """
        return all(np.array(a) < np.array(b))

    # checking if coordinates are inside the array (between (0,0) and (N,N))
    if compare_coordinates((0, 0), moved_position) and compare_coordinates(moved_position, grid.shape):
        # checking if the coordinates are not on the obstacle
        if grid[moved_position] == 'x':
            return False
        else:
            return True
    else:
        return False


def pathfinder(starting_position: tuple, target_position: tuple, grid: np.ndarray) -> List[tuple] or None:
    """
    Path finding function to seek the available path if the 'easy' way fails
    Short description:
        1. Check all possible moves (not in history and not dead ends)
        2. Select the most profitable move (least distance to target)
        3. Move there, add previous position to history and move to path
        4. Go back to 1, if no move is possible, declare position dead end and move to previous position in history
        5. Repeat until the target is reached
    :param starting_position: starting position
    :param target_position: target position
    :param grid: validated array of a grid
    :return: list with available path
    """
    moves_dict = {(1, 0): "DOWN", (-1, 0): "UP", (0, 1): "RIGHT", (0, -1): "LEFT"}

    moves = []
    path = []
    dead_ends = []

    def rate_position(current, target):
        """
        Helper function to calculate distance to target
        """
        return (target[0] - current[0]) ** 2 + (target[1] - current[1]) ** 2

    # Setting starting position
    current_position = starting_position
    while current_position != target_position:
        possible_moves = {}
        # Checking for each possible move and rating them
        for m in moves_dict.keys():
            if check_valid_move(grid, current_position, m):
                new_position = tuple(np.add(current_position, m))
                new_position_rating = rate_position(new_position, target_position)
                if new_position not in path and new_position not in dead_ends:
                    possible_moves[new_position_rating] = m

        # if there are possible move, select the one, that would move us the closest to target
        if possible_moves:
            path.append(current_position)  # save position to path
            moves.append(possible_moves[min(possible_moves)])  # save move to move list
            current_position = tuple(np.add(current_position, possible_moves[min(possible_moves)]))
        # if not, go back one move and add current position to dead ends
        else:
            # if no moves available from the start, return None
            if current_position == starting_position:
                return None
            dead_ends.append(current_position)  # save position to dead ends
            current_position = path[-1]  # move back one step
            path.pop(-1)  # delete step from path
            moves.pop(-1)  # delete move from move list

    return [tuple(moves_dict[move] for move in moves)]


def main(predef_size: int = None, predef_grid: List[str] = None) -> Tuple[bool, List[str] or None]:
    try:
        size = input_grid_size(predef_size)
        grid = input_grid(predef_grid)

        mario_pos, princess_pos, v_grid = parse_grid(grid, size)

        print(v_grid)

        all_paths = get_easy_possible_paths(mario_pos, princess_pos)

        working_paths = find_working_paths(all_paths, mario_pos, v_grid)
        if not working_paths:
            working_paths = pathfinder(mario_pos, princess_pos, v_grid)

        print(working_paths)
        return False, working_paths

    except GridError as e:
        print("Grid is not correctly defined")
        print(e)
        return True, None


if __name__ == "__main__":
    main()
