# import werkzeug
# werkzeug.cached_property = werkzeug.utils.cached_property
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1groups.api import nsGroupManagement
from api.v1groups.models import GroupV1Models
from api.v1groups.group import Group
from api.v1users.user import User


@nsGroupManagement.route('/')
# @auth.login_required
class AuthV1(Resource):
    @jwt_required()
    @nsGroupManagement.response(201, model=GroupV1Models.groupCreate, description='Successfully created group')
    @nsGroupManagement.response(400, model=GroupV1Models.groupErrorMessage, description='Validation Error')
    @nsGroupManagement.response(409, model=GroupV1Models.groupErrorMessage, description='Duplicate Group')
    @nsGroupManagement.doc('Create a user group.')
    @nsGroupManagement.expect(GroupV1Models.groupCreate, validate=True)
    def post(self):
        """Create a new user group."""
        userName = get_jwt_identity()
        data = request.get_json(force=True)
        myGroup = Group()
        data, state = myGroup.create(data=data)
        return data, state


@nsGroupManagement.route('/<string:group>')
class AuthV1(Resource):
    @jwt_required()
    @nsGroupManagement.response(200, model=GroupV1Models.groupOutput, description='Successfully retrived data.')
    @nsGroupManagement.response(204, model=GroupV1Models.groupMessage, description='Success deleted group.')
    @nsGroupManagement.response(400, model=GroupV1Models.groupErrorMessage, description='Validation payload error')
    @nsGroupManagement.response(404, model=GroupV1Models.groupErrorMessage, description='Group not found')
    @nsGroupManagement.doc('Get or delete a user group.')

    def get(self, group):
        """Get information about the group."""
        myGroup = Group()
        if myGroup.search_by_name(name=group):
            version, state = myGroup.get()
            return version, state
        else:
            return {"error": "Group not found."}, 404

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


@nsGroupManagement.route('/<string:group>/user/<string:username>')
class AuthV1(Resource):
    @jwt_required()
    @nsGroupManagement.response(201, model=GroupV1Models.groupCreate, description='Successfully added user to the group.')
    @nsGroupManagement.response(204, model=GroupV1Models.groupMessage, description='Successfully deleted user from group.')
    @nsGroupManagement.response(400, model=GroupV1Models.groupErrorMessage, description='Error occured while adding a user to group')
    @nsGroupManagement.response(404, model=GroupV1Models.groupErrorMessage, description='Username and/or group not found')
    @nsGroupManagement.response(409, model=GroupV1Models.groupErrorMessage, description='User is already part of the group')
    @nsGroupManagement.doc('Group management by adding/removing users.')
    @nsGroupManagement.expect(GroupV1Models.groupCreate, validate=True)

    def post(self, group, username):
        """Adds a user from the usergroup."""
        myUser = User()
        myGroup = Group()
        if myUser.search_by_name(name=username) and myGroup.search_by_name(name=group):
            try:
                if myGroup.is_in_group(username=username):
                    message, groupStatus = myGroup.add_user(username=username)
                    myUser.add_to_group(groupname=group)
                    return {"message": "User added to group."}, 201
                else:
                    return {"error": "User is already part of group."}, 409
            except Exception as e:
                myGroup.remove_user(username=username)
                myUser.remove_from_group(groupname=group)
            if groupStatus:
                return {"message": "Added user to group."}, 201
            else:
                return message, 400
        else:
            return {"error": "Username and/or group not found."}, 404


    def delete(self, group, username):
        """Deletes a user from a usergroup."""
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
