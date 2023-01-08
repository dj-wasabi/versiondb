from flask import request
from flask_restx import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api.v1artifacts.models import artifactV1Output, artifactV1Input
from api.v1artifacts.api import nsArtifact
from api.v1artifacts.artifact import Artifact
from api.v1artifacts.version import Version


@nsArtifact.route('/')
class ArtifactV1(Resource):
    @nsArtifact.response(201, model=artifactV1Input.createArtifact, description='Successfuly created artifact.')
    @nsArtifact.response(400, model=artifactV1Output.artifactErrorMessage, description='Payload validation error')
    @nsArtifact.response(409, model=artifactV1Output.artifactErrorMessage, description='Attempt to a duplicated artifact creation.')
    @nsArtifact.doc('Create an artifact in the database.')
    @nsArtifact.expect(artifactV1Input.createArtifact, validate=True)

    @jwt_required()
    def post(self):
        """Create an artifact."""
        userName = get_jwt_identity()
        data = request.get_json(force=True)
        art = Artifact(data=data)
        version, state = art.create(user=userName)
        return version, state


@nsArtifact.route('/<string:artifact>')
class ArtifactV1(Resource):
    @nsArtifact.response(200, model=artifactV1Input.createArtifact, description='Successfuly retrieved artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.doc('Get all information about the artifact.')

    @jwt_required()
    def get(self, artifact):
        """Get the information for the provided artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.get()
            return version, state
        else:
            return {"error": "Artifact not found."}, 404

    @nsArtifact.response(200, model=artifactV1Input.createArtifact, description='Successfuly patched artifact.')
    @nsArtifact.response(400, model=artifactV1Output.artifactErrorMessage, description='Payload validation error')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.expect(artifactV1Input.createArtifact, validate=True)
    @nsArtifact.marshal_with(artifactV1Input.createArtifact)

    @jwt_required()
    def patch(self, artifact):
        """Patch specific information for the artifact."""
        userName = get_jwt_identity()
        art = Artifact()
        data = request.get_json(force=True)
        if art.search_by_name(name=artifact):
            version, state = art.patch(user=userName, data=data)
            return version, state
        else:
            return {"error": "Artifact not found."}, 404


@nsArtifact.route('/<string:artifact>/patch')
class ArtifactV1Patch(Resource):
    @nsArtifact.response(200, model=artifactV1Output.artifactVersionMessage, description='Successfuly retrieved the next "patch" version of artifact.')
    @nsArtifact.response(201, model=artifactV1Output.artifactVersionMessage, description='Successfuly updated "patch" version artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.doc("Increment the 'patch' version of the artifact with 1.")
    @nsArtifact.marshal_with(artifactV1Output.artifactVersionMessage)

    @jwt_required()
    def get(self, artifact):
        """Get the next 'patch' version of the artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.getNextVersion(name=artifact, type="patch")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404

    @jwt_required()
    def post(self, artifact):
        """Increment the 'patch' version of the artifact with 1."""
        userName = get_jwt_identity()
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.update(name=artifact, user="admin", type="patch")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404


@nsArtifact.route('/<string:artifact>/minor')
class ArtifactV1Minor(Resource):
    @nsArtifact.doc("Increment the 'minor' version of the artifact with 1.")
    @nsArtifact.response(200, model=artifactV1Input.createArtifact, description='Successfuly retrieved the next "minor" version of artifact.')
    @nsArtifact.response(201, model=artifactV1Output.artifactVersionMessage, description='Successfuly updated "minor" version artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.marshal_with(artifactV1Output.artifactVersionMessage)

    @jwt_required()
    def get(self, artifact):
        """Get the next 'minor' version of the artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.getNextVersion(name=artifact, type="minor")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404

    @jwt_required()
    def post(self, artifact):
        """Increment the 'minor' version of the artifact with 1."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.update(name=artifact, user="admin", type="minor")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404


@nsArtifact.route('/<string:artifact>/major')
class ArtifactV1tMajor(Resource):
    @nsArtifact.doc("Increment the 'major' version of the artifact with 1.")
    @nsArtifact.response(200, model=artifactV1Input.createArtifact, description='Successfuly retrieved the next "major" version of artifact.')
    @nsArtifact.response(201, model=artifactV1Output.artifactVersionMessage, description='Successfuly updated "major" version artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.marshal_with(artifactV1Output.artifactVersionMessage)

    @jwt_required()
    def get(self, artifact):
        """Get the next 'major' version of the artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.getNextVersion(name=artifact, type="major")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404

    @jwt_required()
    def post(self, artifact):
        """Increment the 'major' version of the artifact with 1."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.update(name=artifact, user="admin", type="major")
            return version, state
        else:
            return {"error": "Artifact not found."}, 404


@nsArtifact.route('/<string:artifact>/versions')
class versionV1Versions(Resource):
    @nsArtifact.doc("Get overview of all versions of this artifact")
    @nsArtifact.response(200, model=artifactV1Input.createArtifact, description='Successfuly retrieved version of artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')
    @nsArtifact.marshal_with(artifactV1Input.artifactVersionsMessage)

    @jwt_required()
    def get(self, artifact):
        """Get the current/latest version of the artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            version, state = art.getAllVersions()
            return version, state
        else:
            return {"error": "Artifact not found."}, 404


@nsArtifact.route('/<string:artifact>/version/<string:version>')
class ArtifactV1Version(Resource):
    @nsArtifact.doc("Artifact version management.")
    @nsArtifact.response(200, model=artifactV1Output.overviewVersion, description='Successfuly retrieved version of artifact.')
    @nsArtifact.response(404, model=artifactV1Output.artifactErrorMessage, description='Artifact does not exist')

    @jwt_required()
    def get(self, artifact, version):
        """Get information about a specific version of the artifact."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            v = Version()
            if v.search_by_name(name=artifact, version=version):
                data, state = v.get()
                return data, state
            else:
                return {"error": "Version not found."}, 404
        else:
            return {"error": "Artifact not found."}, 404

    @jwt_required()
    def patch(self, artifact, version):
        """Update specific information on a version."""
        # userName = get_jwt_identity()
        patchdata = request.get_json(force=True)
        art = Artifact()
        if art.search_by_name(name=artifact):
            v = Version()
            if v.search_by_name(name=artifact, version=version):
                data, state = v.update(user="admin", data=patchdata)
                return data, state
            else:
                return {"error": "Version not found."}, 404
        else:
            return {"error": "Artifact not found."}, 404

    @jwt_required()
    def delete(self, artifact, version):
        """Delete the provided version."""
        art = Artifact()
        if art.search_by_name(name=artifact):
            v = Version()
            if v.search_by_name(name=artifact, version=version):
                data, state = v.delete()
                return data, state
            else:
                return {"error": "Version not found."}, 404
        else:
            return {"error": "Artifact not found."}, 404
