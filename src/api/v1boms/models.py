from flask_restx import Api, fields
from api.v1boms.api import nsBom


class bomV1Serials():

    bomOutput = nsBom.model('Bom', {
        'name': fields.String(description="The name of the artifact."),
        'version': fields.String(default="0.0.0", description="The version to start with."),
        'artifacts': fields.Raw(),
    }, strict=True)
