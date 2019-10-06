import random
import requests
from mario import main
import sql_handle


def create_random_grid(grid_size):
    """
    Create random grid with possibility of unacceptable sign ('t')
    :param grid_size: size of generated grid
    :return: grid
    """
    grid = []
    mario_position = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    princess_position = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    while mario_position == princess_position:
        princess_position = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    for n in range(grid_size):
        row = [random.choice(['-', '-', 'x', 'x', '-', '-', '-', 'x', 'x', '-', 't']) for m in range(grid_size)]
        grid.append(row)
    grid[mario_position[0]][mario_position[1]] = 'm'
    grid[princess_position[0]][princess_position[1]] = 'p'
    grid = [''.join(row) for row in grid]
    return grid


# TESTING THE GAME ITSELF
def test_game():
    # creating database
    engine, session, base = sql_handle.create_database()
    entries = sql_handle.create_entries_table(engine, base)

    # creating, validating and trying to solve 10 random grids
    # outputting results to database
    for i in range(10):
        size = random.randint(3, 5)

        grid = create_random_grid(size)
        print(grid)
        error_flag, paths = main(size, grid)

        entry = dict(id=i, grid_size=size, grid=','.join(grid), error_flag=error_flag,
                     path=','.join(paths[0]) if paths is not None else None)
        sql_handle.add_entry(session, entries, entry)

    # getting results and results count
    count = sql_handle.select_count_from(session, entries)
    print(count)

    results = sql_handle.select_all_from(session, entries)
    for row in results:
        print(row)

    return count


# testing the REST API

LOCAL_URL = "http://127.0.0.1:5000/"


def get_request(url):
    return requests.get(url)


def post_request(url, data):
    return requests.post(url, data)


def test_rest():
    response = post_request(LOCAL_URL, {'grid_size': 5, 'grid': create_random_grid(5)})
    print(response.json())

    game_id = int(response.json()["game_id"])

    print(game_id)

    results = get_request(LOCAL_URL)

    print(results.json())

    return game_id


if __name__ == "__main__":
    games_count = test_game()
    if games_count == 10:
        print('='*20)
        print("Game test is a success")
        print('=' * 20)
    # you need to start rest_api.py before that line
    last_game_id = test_rest()
    if last_game_id == 10:
        print('=' * 20)
        print("REST API test is a success")
        print('=' * 20)
