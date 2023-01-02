from flask_restx import fields
from api.v1users.api import nsUserManagement


class UserV1Models():
    userAuthentication = nsUserManagement.model('userAuthentication', {
        'username': fields.String(description="The username of the user to authenticate."),
        'password': fields.String(description="The password for the user.")
    }, strict=True)
    userGetOutput = nsUserManagement.model('userGetOutput', {
        'is_active': fields.Boolean(default=True, description="If a user is active or not."),
        'created_date': fields.DateTime(description="The date in EPOCH when the user is created"),
        'username': fields.String(description="The username of the user to authenticate."),
        'groups': fields.List(fields.String)
    }, strict=True)
    userRegistration = nsUserManagement.model('userRegistration', {
        'is_active': fields.Boolean(default=True, description="If a user is active or not."),
        'username': fields.String(description="The username of the user to authenticate."),
        'password': fields.String(description="The password for the user."),
        'groups': fields.List(fields.String)
    }, strict=True)
    userMessage = nsUserManagement.model('userMessage', {
        'message': fields.String(description="Notification message."),
    }, strict=True)
    userErrorMessage = nsUserManagement.model('userErrorMessage', {
        'error': fields.String(description="The Error message"),
    }, strict=True)
    userLogin = nsUserManagement.model('userLogin', {
        'token': fields.String(description="The access_token which is needed for authentication."),
    }, strict=True)
