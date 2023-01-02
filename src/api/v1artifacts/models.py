from flask_restx import Api, fields
from api.v1artifacts.api import nsArtifact


class ArtifactV1Models():
    metadata = nsArtifact.model('Metadata', {
        'key': fields.String(readOnly=True, description="The key name of the metadata option."),
        'value': fields.String(readOnly=True, description="The value for the metadata.")
    })
    metaVersions = nsArtifact.model('metaVersions', {
        'version': fields.String(readOnly=True, description="The version."),
        'created': fields.String(readOnly=True, description="The date when version was created (epoch).")
    })
    createArtifact = nsArtifact.model('Artifact', {
        'name': fields.String(description="The name of the artifact."),
        'category': fields.String(description="The name of the category."),
        'url': fields.String(description="URL that provides some information."),
        'git': fields.String(description="The GIT URL either http(s) or git."),
        'version': fields.String(default="0.0.0", description="The version to start with."),
        'metadata': fields.List(fields.Nested(metadata)),
    }, strict=True)
    artifactErrorMessage = nsArtifact.model('artifactErrorMessage', {
        'error': fields.String(description="The Error message"),
    }, strict=True)
    artifactVersionsMessage = nsArtifact.model('artifactVersionsMessage', {
        'versions': fields.List(fields.Nested(metaVersions)),
    }, strict=True)
    artifactVersionMessage = nsArtifact.model('artifactVersionMessage', {
        'version': fields.String(description="The version value."),
    }, strict=True)
    overviewVersion = nsArtifact.model('overviewVersion', {
        'name': fields.String(description="The name of the artifact."),
        'version': fields.String(description="The version of the artifact."),
        'shasum': fields.String(description="The 'shasum' of the artifact belonging to this version."),
        'commit': fields.String(description="The 'shasum' of the artifact belonging to this version."),
        'created_by': fields.String(description="The username that has created the version."),
        'created_date': fields.DateTime(description="The date in EPOCH when the version is created"),
        'updated_by': fields.String(description="The last username that has updated the version."),
        'updated_date': fields.DateTime(description="The last EPOCH time when version is updated."),
    }, strict=True)
