from http import HTTPStatus
import time
from flask import Flask, request, Response, json, after_this_request
from flask_restful import Resource, Api
import sql_handle
from mario import main


app = Flask(__name__)
api = Api(app)


def create_response(data, status):
    """
    Simple function to create responses
    """
    return Response(response=json.dumps(data), status=status, mimetype='application/json')


class Game(Resource):
    """
    Class for Game endpoint to post game settings and get game results
    """
    def get(self):
        """
        Get game settings and results from database
        """
        game_info = sql_handle.select_all_from(session, entries)

        response_data = game_info
        status = HTTPStatus.OK
        return create_response(response_data, status)

    def post(self):
        """
        Post new game settings and get in response the appropriate game result
        """
        before = time.time()
        # getting game settings
        game_settings = request.form.to_dict(flat=False)
        grid = game_settings["grid"]
        grid_size = game_settings["grid_size"][0]

        # assigning game id
        game_id = sql_handle.select_count_from(session, entries)

        # getting game result
        error_flag, paths = main(grid_size, grid)

        # outputting game results to row dictionary
        entry = dict(id=game_id, grid_size=grid_size, grid=','.join(grid), error_flag=error_flag,
                     path=','.join(paths[0]) if paths is not None else None)

        # returning game result
        response_data = {"game_id": game_id, "results": {"error_flag": error_flag, "paths": paths}}
        status = HTTPStatus.ACCEPTED

        # after request is completed, add new row to the database along with request time
        @after_this_request
        def add_entry(response):
            request_time = time.time() - before
            entry["request_time"] = request_time
            sql_handle.add_entry(session, entries, entry)
            return response

        return create_response(response_data, status)


# mapping classes to roles' URLs
api.add_resource(Game, '/')

if __name__ == '__main__':
    # creating a DB
    engine, session, base = sql_handle.create_database()
    entries = sql_handle.create_entries_table(engine, base)
    # starting an app
    app.run(port=5000)
