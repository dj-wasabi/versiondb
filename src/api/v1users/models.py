from flask_restx import fields
from api.v1users.api import nsUserManagement


class userV1Output():
    userGetData = nsUserManagement.model('userGetData', {
        'is_active': fields.Boolean(default=True, description="If a user is active or not."),
        'created_date': fields.Integer(description="The date in EPOCH when the user is created"),
        'username': fields.String(description="The username of the user to authenticate."),
        'groups': fields.List(fields.String)
    }, strict=True)
    userErrorMessage = nsUserManagement.model('userErrorMessage', {
        'error': fields.String(description="The Error message"),
    }, strict=True)
    userMessage = nsUserManagement.model('userMessage', {
        'message': fields.String(description="Notification message."),
    }, strict=True)
    userAuthenticationToken = nsUserManagement.model('userAuthenticationToken', {
        'token': fields.String(description="The access_token which is needed for authentication."),
    }, strict=True)
    usernoAuthentication = nsUserManagement.model('usernoAuthentication', {
        'msg': fields.String(description="Missing Authorization Header"),
    }, strict=True)

class userV1Input():
    userRegistration = nsUserManagement.model('userRegistration', {
        'is_active': fields.Boolean(default=True, description="If a user is active or not."),
        'username': fields.String(description="The username of the user to authenticate."),
        'password': fields.String(description="The password for the user."),
        'groups': fields.List(fields.String)
    }, strict=True)
    userAuthentication = nsUserManagement.model('userAuthentication', {
        'username': fields.String(description="The username of the user to authenticate."),
        'password': fields.String(description="The password for the user.")
    }, strict=True)
