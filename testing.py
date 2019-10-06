import random
from mario import main
import sql


def create_random_grid(grid_size):
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


test = ["--m, -xx, --p"]

print(test[0][2])

engine, session, base = sql.create_database()
entries = sql.create_entries_table(engine, base)

for i in range(10):
    size = random.randint(3, 5)

    grid = create_random_grid(size)

    error_flag, paths = main(size, grid)

    entry = dict(id=i, grid_size=size, grid=','.join(grid), error_flag=error_flag,
                 path=','.join(paths[0]) if paths is not None else None)
    sql.add_entry(session, entries, entry)

results = sql.select_all_from(session, entries)
for row in results:
    print(row)
