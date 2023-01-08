from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1boms.models import bomV1Serials
from api.v1boms.api import nsBom
from api.v1boms.bom import Bom


@nsBom.route('/category/<string:category>')
class myBom(Resource):
    @nsBom.response(200, 'Success')
    @nsBom.response(200, model=bomV1Serials.bomOutput, description='Successfuly provided information.')
    @nsBom.marshal_with(bomV1Serials.bomOutput)

    @jwt_required()
    def get(self, category):
        """Generates a Bill of Materials for a specific category."""
        bom = Bom()
        if bom.search_by_name(name=category):
            return bom.get_latest()
        else:
            return {"error": "Category not found."}, 404


@nsBom.route('/category/<string:category>/patch')
class myBom(Resource):
    @nsBom.response(200, 'Success')

    @jwt_required()
    def post(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        userName = get_jwt_identity()
        bom = Bom()
        if bom.search_by_name(name=category):
            return bom.patchBom(user=userName)
        else:
            return {"error": "Category not found."}, 404


@nsBom.route('/category/<string:category>/minor')
class myBom(Resource):
    @nsBom.response(200, 'Success')

    @jwt_required()
    def post(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        userName = get_jwt_identity()
        bom = Bom()
        if bom.search_by_name(name=category):
            return bom.minorBom(user=userName)
        else:
            return {"error": "Category not found."}, 404


@nsBom.route('/category/<string:category>/major')
class myBom(Resource):
    @nsBom.response(200, 'Success')

    @jwt_required()
    def post(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        userName = get_jwt_identity()
        bom = Bom()
        if bom.search_by_name(name=category):
            return bom.majorBom(user=userName)
        else:
            return {"error": "Category not found."}, 404


@nsBom.route('/category/<string:category>/versions')
class myBom(Resource):
    @nsBom.response(200, 'Success')

    @jwt_required()
    def get(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        bom = Bom()
        bom.search_by_name(name=category)
        return bom.get_current(category=category)


@nsBom.route('/category/<string:category>/version/<string:version>')
class myBom(Resource):
    @nsBom.response(200, 'Success')

    @jwt_required()
    def get(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        bom = Bom()
        bom.search_by_name(name=category)
        return bom.get_current(category=category)


    @jwt_required()
    def patch(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        bom = Bom()
        bom.search_by_name(name=category)
        return bom.get_current(category=category)


    @jwt_required()
    def delete(self, category):
        """Create a Bill of Materials with all categorys and artifacts."""
        bom = Bom()
        bom.search_by_name(name=category)
        return bom.get_current(category=category)
