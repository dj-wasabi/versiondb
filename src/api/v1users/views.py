from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1users.api import nsUserManagement
from api.v1users.models import userV1Output, userV1Input
from api.v1users.user import User
from api.v1groups.group import Group


@nsUserManagement.route('/<string:username>')
class AuthV1(Resource):
    @nsUserManagement.response(200, model=userV1Output.userGetData, description='Success')
    @nsUserManagement.response(200, model=userV1Output.userGetData, description='Success')
    @nsUserManagement.response(401, model=userV1Output.usernoAuthentication, description='Authentication issue with missing the token in header')
    @nsUserManagement.response(404, model=userV1Output.userErrorMessage, description='User not found')
    @nsUserManagement.doc('Getting information about the provided username.')
    @nsUserManagement.marshal_with(userV1Output.userGetData)

    @jwt_required()
    def get(self, username):
        """Get overview of all available data about the provided user."""
        myUser = User()
        if myUser.search_by_name(name=username):
            message, state = myUser.get()
            return message, state
        else:
            return {"error": "User not found."}, 404


@nsUserManagement.route('/authenticate')
class AuthV1(Resource):
    @nsUserManagement.response(200, model=userV1Output.userAuthenticationToken, description='Successfully authenticated.')
    @nsUserManagement.response(401, model=userV1Output.userErrorMessage, description='Error occured during authentication.')
    @nsUserManagement.doc('Authenticate an existing user.')
    @nsUserManagement.expect(userV1Input.userAuthentication, validate=True)
    def post(self):
        """Authenticate an existing user."""
        data = request.get_json(force=True)
        authRequest = User()
        message, state = authRequest.authenticateUser(data=data)
        return message, state


@nsUserManagement.route('/register')
# @auth.login_required
class AuthV1(Resource):
    @nsUserManagement.response(201, model=userV1Output.userGetData, description='Successfully created.')
    @nsUserManagement.response(400, model=userV1Output.userErrorMessage, description='Validation payload error.')
    @nsUserManagement.response(409, model=userV1Output.userErrorMessage, description='Attempt to a duplicated user registration.')
    @nsUserManagement.doc('Create a new user account.')
    @nsUserManagement.expect(userV1Input.userRegistration, validate=True)

    def post(self):
        """Register or create a new user."""
        data = request.get_json(force=True)
        myauth = User(data=data)
        if not myauth.search_by_name(name=data["username"]):
            return myauth.create(password=data["password"])
        else:
            return {"error": "Username is already taken."}, 409


@nsUserManagement.route('/<string:username>/group/<string:group>')
# @auth.login_required
class AuthV1(Resource):
    @nsUserManagement.response(201, model=userV1Output.userMessage, description='Successfully added group to the user.')
    @nsUserManagement.response(400, model=userV1Output.userErrorMessage, description='Validation payload error')
    @nsUserManagement.response(401, model=userV1Output.usernoAuthentication, description='Authentication issue with missing the token in header')
    @nsUserManagement.response(404, model=userV1Output.userErrorMessage, description='Username and/or group not found')
    @nsUserManagement.response(409, model=userV1Output.userErrorMessage, description='User is already part of the group.')
    @nsUserManagement.doc('Group management by adding/removing users.')

    @jwt_required()
    def post(self, group, username):
        """Add a user to the provided usergroup."""
        myUser = User()
        myGroup = Group()
        if myUser.search_by_name(name=username) and myGroup.search_by_name(name=group):
            try:
                if not myGroup.is_in_group(username=username):
                    message, groupStatus = myGroup.add_user(username=username)
                    myUser.add_to_group(groupname=group)
                    return {"message": "User added to group."}, 201
                else:
                    return {"error": "User is already part of the group."}, 409
            except Exception as e:
                myGroup.remove_user(username=username)
                myUser.remove_from_group(groupname=group)
            if groupStatus:
                return {"message": "Added user to group."}, 201
            else:
                return message, 400
        else:
            return {"error": "Username and/or group not found."}, 404

    @nsUserManagement.response(204, model=userV1Output.userMessage, description='Successfully deleted')
    @nsUserManagement.response(400, model=userV1Output.userErrorMessage, description='Validation payload error')
    @nsUserManagement.response(401, model=userV1Output.usernoAuthentication, description='Authentication issue with missing the token in header')
    @nsUserManagement.response(404, model=userV1Output.userErrorMessage, description='Username and/or group not found')
    
    @jwt_required()
    def delete(self, group, username):
        """Removes the user from the provided group."""
        myUser = User()
        myGroup = Group()
        if myUser.search_by_name(name=username) and myGroup.search_by_name(name=group):
            message, state = myGroup.remove_user(username=username)
            myUser.remove_from_group(groupname=group)
            if state:
                return {}, 204
            else:
                return message, 400
        else:
            return {"error": "Username and/or group not found."}, 404
