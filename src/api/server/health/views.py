# from flask import request, make_response, jsonify
from flask_restx import Resource

from api.server.health.api import nsHealth
from api.server.health.api import health
from api.server.mongodb.mongodb import client
import json


def mongodb_check():
    try:
        client.admin.command('ping')
        return True, "MongoDB connection working fine"
    except ConnectionFailure:
        return False, "MongoDB connection/server not available"


health.add_check(mongodb_check)


@nsHealth.route('/alive')
class AuthV1(Resource):
    def get(self):
        """Get the alive check to see if the process is healthy."""
        
        return json.loads(health.run()[0]), health.run()[1]

