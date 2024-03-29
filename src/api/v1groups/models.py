from flask_restx import fields
from api.v1groups.api import nsGroupManagement

class groupV1Input():
    groupCreate = nsGroupManagement.model('groupCreate', {
        'name': fields.String(description="The name of the group.")
    }, strict=True)


class groupV1Output():
    groupNoAuthentication = nsGroupManagement.model('groupNoAuthentication', {
        'msg': fields.String(description="Missing Authorization Header"),
    }, strict=True)
    groupErrorMessage = nsGroupManagement.model('groupErrorMessage', {
        'error': fields.String(description="An error message explaining what when wrong."),
    }, strict=True)
    groupCreate = nsGroupManagement.model('groupCreate', {
        'name': fields.String(description="The name of the group.")
    }, strict=True)
    groupOutput = nsGroupManagement.model('groupOutput', {
        'name': fields.String(description="The name of the group."),
        'created_date': fields.DateTime(description="The date in EPOCH when the group is created"),
        'users': fields.List(fields.String(description="The users that are part of this group.", default=""))
    }, strict=True)
    groupDelete = nsGroupManagement.model('groupDelete', {}, strict=True)
