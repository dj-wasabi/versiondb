# import werkzeug
# werkzeug.cached_property = werkzeug.utils.cached_property
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1groups.api import nsGroupManagement
from api.v1groups.models import groupV1Input, groupV1Output, groupV1Output
from api.v1groups.group import Group
from api.v1users.user import User


@nsGroupManagement.route('/')
# @auth.login_required
class AuthV1(Resource):
    @nsGroupManagement.response(201, model=groupV1Output.groupCreate, description='Successfully created group')
    @nsGroupManagement.response(400, model=groupV1Output.groupErrorMessage, description='Validation Error')
    @nsGroupManagement.response(401, model=groupV1Output.groupNoAuthentication, description='Authentication issue with missing the token in header')
    @nsGroupManagement.response(409, model=groupV1Output.groupErrorMessage, description='Duplicate Group')
    @nsGroupManagement.doc('Create a user group.')
    @nsGroupManagement.expect(groupV1Input.groupCreate, validate=True)

    @jwt_required()
    def post(self):
        """Create a new user group."""
        userName = get_jwt_identity()
        data = request.get_json(force=True)
        myGroup = Group()
        data, state = myGroup.create(data=data)
        return data, state


@nsGroupManagement.route('/<string:group>')
class AuthV1(Resource):
    @nsGroupManagement.response(200, model=groupV1Output.groupOutput, description='Successfully retrived data.')
    @nsGroupManagement.response(400, model=groupV1Output.groupErrorMessage, description='Validation payload error')
    @nsGroupManagement.response(401, model=groupV1Output.groupNoAuthentication, description='Authentication issue with missing the token in header')
    @nsGroupManagement.response(404, model=groupV1Output.groupErrorMessage, description='Group not found')
    @nsGroupManagement.doc('Get or delete a user group.')

    @jwt_required()
    def get(self, group):
        """Get information about the group."""
        myGroup = Group()
        if myGroup.search_by_name(name=group):
            version, state = myGroup.get()
            return version, state
        else:
            return {"error": "Group not found."}, 404

    @nsGroupManagement.response(204, model=groupV1Output.groupDelete, description='Success deleted group.')
    @nsGroupManagement.response(401, model=groupV1Output.groupNoAuthentication, description='Authentication issue with missing the token in header')
    @nsGroupManagement.response(404, model=groupV1Output.groupErrorMessage, description='Group not found')
    @jwt_required()
    def delete(self, group):
        """Delete the group."""
        myGroup = Group()
        if myGroup.search_by_name(name=group):
            for user in myGroup.users:
                myUser = User()
                myUser.search_by_name(name=user)
                myUser.remove_from_group(groupname=group)
            version, state = myGroup.delete()
            return version, state
        else:
            return {"error": "Group not found."}, 404
