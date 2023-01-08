from flask_restx import Api, fields
from api.v1boms.api import nsBom


class bomV1Serials():

    bomOutput = nsBom.model('Bom', {
        'name': fields.String(description="The name of the artifact."),
        'artifacts': fields.Raw(),
    }, strict=True)
