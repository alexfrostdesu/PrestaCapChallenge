# Maze game and RESTful API challenge

This is a simple maze game with basic pathfinding and RESTful API Flask app to play it

## Installation

```bash
git clone https://github.com/alexfrostdesu/PrestaCapChallenge.git
cd PrestaCapChallenge
pip install -r requirements.txt
python mario.py
```

## Testing

There are some testing scripts to provide basic testing for this app (with and without Flask)

```bash
python testing.py
```

## Usage
### Game
You have two inputs `N` which is the grid size, and `Grid` which is the actual map itself.
`N` is a scalar integer, while `Grid` should be a list of strings, where each entry is a row of the map itself.
Example:

N = 3

Grid = ['--m', '-x-', '-p-']
```
- - m
- x - 
- p -
```

App will validate your inputs and attempts to find the shortest routes.

If grid is not correctly defined, it will return `error_flag = True`, otherwise `error_flag` would be equal `False`.

If grid is correct, app would attempt to find the the route and would return `paths` equal to list of shortest routes. 
If no path is available, `paths` would be equal `None`

Run `python mario.py` to try the game out itself.

### Flask RESTful API

After running `rest_api.py` script, you can interact with the game via `POST` and `GET` requests sent to `localhost:5000`.
Sending a `POST` request with body of request defined like this `{'grid_size': 3, 'grid': ['--m', '-x-', '-p-']}` 
would return the same results as the game itself.

You can use `GET` method to get all games definitions and results from current session.

### Serverless database (SQLite)

This game uses serverless database to store game results. This database would be created in `/tmp/dbmario.db` relative path file.

## License
[MIT](https://opensource.org/licenses/MIT)