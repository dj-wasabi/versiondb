from flask_restx import fields
from api.v1categories.api import nsCategory


class categoryV1Output():
    categoryGet = nsCategory.model('categoryoverviewVersion', {
        'name': fields.String(description="The name of the category."),
        'created_by': fields.String(description="The username that has created the version."),
        'created_date': fields.DateTime(description="The date in EPOCH when the version is created"),
        'updated_by': fields.String(description="The last username that has updated the version."),
        'updated_date': fields.DateTime(description="The last EPOCH time when version is updated."),
    }, strict=True)
    categoryErrorMessage = nsCategory.model('categoryErrorMessage', {
        'error': fields.String(description="The Error message"),
    }, strict=True)
    categoryVersionMessage = nsCategory.model('categoryVersionMessage', {
        'version': fields.String(description="The version value."),
    }, strict=True)
    categoryNoAuthentication = nsCategory.model('categoryNoAuthentication', {
        'msg': fields.String(description="Missing Authorization Header"),
    }, strict=True)

class categoryV1Input():
    categoryCreate = nsCategory.model('categoryCreate', {
        'name': fields.String(description="The name of the category."),
    }, strict=True)

    categoryPatch = nsCategory.model('categoryPatch', {
        'category': fields.String(description="The name of the category."),
        'url': fields.String(description="URL that provides some information."),
        'git': fields.String(description="The GIT URL either http(s) or git."),
        'version': fields.String(default="0.0.0", description="The version to start with."),
    }, strict=True)

    categoryMetaVersions = nsCategory.model('categoryMetaVersions', {
        'version': fields.String(readOnly=True, description="The version."),
        'created': fields.String(readOnly=True, description="The date when version was created (epoch).")
    })
    categoryVersionsMessage = nsCategory.model('categoryVersionsMessage', {
        'versions': fields.List(fields.Nested(categoryMetaVersions)),
    }, strict=True)
    categoryVersionMessage = nsCategory.model('categoryVersionMessage', {
        'version': fields.String(description="The version value."),
    }, strict=True)
