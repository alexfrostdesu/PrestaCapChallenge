from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from http import HTTPStatus
import sql_handle
from mario import main


app = Flask(__name__)
api = Api(app)

response_messages = {'not_ready': "Results not ready",
                     'bid_low': "Bid is too low",
                     'item_not_found': "Item not found",
                     'user_not_found': "User not found",
                     'no_list_sent': "No item found in sent list",
                     'auction_not_started': "Auction have not started yet"}


def create_response(data, status):
    """
    Simple function to create responses
    """
    return Response(response=json.dumps(data), status=status, mimetype='application/json')


class Game(Resource):
    """
    Class for Auctioneer role to create item bidding list and initiate bid award process
    """
    def get(self):
        """
        Initiates bid award process
        Returns the result
        """

        status = HTTPStatus.OK
        return create_response(response_data, status)

    def post(self):
        """
        Creates item bidding list
        """
        # getting new item bidding list
        game_props = request.form.to_dict()
        print(game_props)
        id = sql_handle.select_count_from(session, entries)
        grid = game_props["grid"].split(',')
        grid_size = game_props['grid_size']
        error_flag, paths = main(grid_size, grid)
        print(paths, error_flag)
        entry = dict(id=id, grid_size=grid_size, grid=','.join(grid), error_flag=error_flag,
                     path=','.join(paths[0]) if paths is not None else None)
        sql_handle.add_entry(session, entries, entry)
        # if item_list:
        #     # adding each item
        #     for item in item_list:
        #         bidding_ds.save_items(item_id=item, value={'starting_bid': float(item_list[item]),
        #                                                    'lowest_bidder': None,
        #                                                    'lowest_bid': None})
        #     # creating a response
        #     response_data = bidding_ds.get_items()
        #     status = HTTPStatus.ACCEPTED
        # else:
        #     response_data = response_messages['no_list_sent']
        #     status = HTTPStatus.BAD_REQUEST
        response_data = {id: game_props}
        status = HTTPStatus.ACCEPTED
        return create_response(response_data, status)


# mapping classes to roles' URLs
api.add_resource(Game, '/')

if __name__ == '__main__':
    # creating a DB
    engine, session, base = sql_handle.create_database()
    entries = sql_handle.create_entries_table(engine, base)
    app.run(port=5000)
