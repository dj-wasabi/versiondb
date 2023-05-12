from flask import request
from flask_restx import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.v1categories.api import nsCategory
from api.v1categories.models import categoryV1Input, categoryV1Output
from api.v1categories.category import Category


@nsCategory.route('/')
class ArtifactV1(Resource):
    @nsCategory.response(201, description='Successfuly created category.')
    @nsCategory.response(400, description='Payload validation error')
    @nsCategory.response(401, description='Authentication issue with missing the token in header')
    @nsCategory.response(409, description='Attempt to a duplicated category creation.')
    @nsCategory.doc('Create a category in the database.')
    @nsCategory.expect(categoryV1Input.categoryCreate, validate=True)

    @jwt_required()
    def post(self):
        """Create a category."""
        userName = get_jwt_identity()
        data = request.get_json(force=True)
        art = Category(data=data)
        version, state = art.create(user=userName)
        return version, state


    @jwt_required()
    def get(self):
        """Get all categories."""
        art = Category()
        data, state = art.get_all()
        return data, state


@nsCategory.route('/<string:category>')
class ArtifactV1(Resource):
    @nsCategory.response(200, model=categoryV1Output.categoryGet, description='Successfuly retrieved category.')
    @nsCategory.response(401, model=categoryV1Output.categoryNoAuthentication, description='Authentication issue with missing the token in header')
    @nsCategory.response(404, model=categoryV1Output.categoryErrorMessage, description='Category does not exist')
    @nsCategory.doc('Get all information about the category.')

    @jwt_required()
    def get(self, category):
        """Get the information for the provided category."""
        cat = Category()
        if cat.search_by_name(name=category):
            version, state = cat.get()
            return version, state
        else:
            return {"error": "Category not found."}, 404

    @jwt_required()
    def delete(self, category):
        """Delete an category."""
        cat = Category()
        if cat.search_by_name(name=category):
            version, state = cat.delete()
            return version, state
        else:
            return {"error": "Category not found."}, 404
