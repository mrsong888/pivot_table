from flask import request
from flask_restful import Resource

from avc_analysis.extensions import block


class DataBlockResource(Resource):
    """ data block resource
    """

    def post(self):
        token, userId = request.headers['Authorization'], request.headers['userId']
        obj = request.json
        url = obj['blockUrl']
        return block.load_block(url, token, userId)

class DataBlockSync(Resource):
    """ single data block sync
    """

    def post(self):
	token, userId = request.headers['Authorization'], request.headers['userId']
        url = obj['blockUrl']
        return block.sync_block(url, token, userId)

class DataBlockAllSync(Resource):
    """ all data block resource sync
        """

    def post(self):
	token, userId = request.headers['Authorization'], request.headers['userId']
        obj = request.json
        url = obj['blockUrl']
        return block.sync_all_blocks(url, token, userId)
