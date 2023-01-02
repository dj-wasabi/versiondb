from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1boms.models import bomV1Serials
from api.v1boms.api import nsBom
from api.v1boms.bom import Bom


@nsBom.route('/all')
class myBom(Resource):
    @jwt_required()
    @nsBom.response(200, 'Success')
    def get(self):
        """Generates a Bill of Materials of all groups and their artifacts."""
        bom = Bom()
        return bom.get_current()


@nsBom.route('/group/<string:group>')
class myBom(Resource):
    @jwt_required()
    @nsBom.response(200, 'Success')
    @nsBom.marshal_with(bomV1Serials.bomOutput)
    def get(self, group):
        """Generates a Bill of Materials for a specific group."""
        bom = Bom()
        bom.search_by_name(name=group)
        return bom.get_latest()


@nsBom.route('/group/<string:group>/patch')
class myBom(Resource):
    @jwt_required()
    @nsBom.response(200, 'Success')
    def put(self, group):
        """Create a Bill of Materials with all groups and artifacts."""
        userName = get_jwt_identity()
        bom = Bom()
        bom.search_by_name(name=group)
        return bom.patchBom(user=userName)


@nsBom.route('/group/<string:group>/minor')
class myBom(Resource):
    @jwt_required()
    @nsBom.response(200, 'Success')
    def put(self, group):
        """Create a Bill of Materials with all groups and artifacts."""
        bom = Bom()
        bom.search_by_name(name=group)
        return bom.get_current(group=group)


@nsBom.route('/group/<string:group>/major')
class myBom(Resource):
    @jwt_required()
    @nsBom.response(200, 'Success')
    def put(self, group):
        """Create a Bill of Materials with all groups and artifacts."""
        bom = Bom()
        bom.search_by_name(name=group)
        return bom.get_current(group=group)
