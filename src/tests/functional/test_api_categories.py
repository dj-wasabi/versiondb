import json

def test_get_category_not_exist(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/api/v1/categories/idonotexist', headers=authentication_headers)
    assert response.status_code == 404
    assert response.json == {"error": "category not found."}


def test_create_category_wrong_post_data(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    postdict = {
        "name": "categoryname",
        "groups": "wrongkeyname"
    }
    response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 400
    assert data["errors"][""] == "Additional properties are not allowed ('groups' was unexpected)"


# def test_create_category_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     postdict = {
#         "name": "categoryname",
#         "category": "category"
#     }
#     response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 401


# def test_create_category(test_client, authentication_headers):
#     """Create an category"""
#     postdict = {
#         "name": "categoryname",
#         "category": "mycategory"
#     }
#     response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data['name'] == "categoryname"
#     assert data['version'] == "0.0.0"
#     assert data['metadata'] == []


# def test_create_category_specify_version(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     postdict = {
#         "name": "categoryversion",
#         "category": "mycategory",
#         "version": "0.1.3"
#     }
#     response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data['name'] == "categoryversion"
#     assert data['version'] == "0.1.3"
#     assert data['metadata'] == []


# def test_patch_category(test_client, authentication_headers):
#     """Update the 'patch' version."""
#     response = test_client.post('/api/v1/categories/categoryname/patch', headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data['version'] == "0.0.1"


# def test_patch_category_unauthenticated(test_client):
#     """Try to update the 'patch' version while not being authenticated."""
#     response = test_client.post('/api/v1/categories/categoryname/patch', headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 401


# def test_patch_category_2(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/categories/categoryversion/patch', headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data['version'] == "0.1.4"


# def test_get_category_get_all_versions(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/categories/categoryname/versions', headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 200
#     assert 'versions' in data
#     assert data["versions"][0]["version"] == "0.0.0"


# def test_minor_category(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/categories/categoryname/minor', headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 201
#     assert data['version'] == "0.1.1"


# def test_minor_category_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/categories/categoryname/minor', headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 401


# def test_major_category(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/categories/categoryname/major', headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data['version'] == "1.0.1"


# def test_major_category_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/categories/categoryname/major', headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 401

# def test_category_get_version(test_client, authentication_headers):
#     """Get specific version of category."""
#     response = test_client.get('/api/v1/categories/categoryname/version/0.0.0', headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 200
#     assert data["name"] == "categoryname"
#     assert data["version"] == "0.0.0"


# def test_category_patch_version(test_client, authentication_headers):
#     """Get specific version of category."""
#     patchdict = {
#         "shasum": "24cdaecc1acf91894b13fb46fedfd179ea7f88c8"
#     }
#     response = test_client.patch('/api/v1/categories/categoryname/version/0.0.0', data=json.dumps(patchdict), headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 200
#     assert data["name"] == "categoryname"
#     assert data["version"] == "0.0.0"
#     assert data["shasum"] == "24cdaecc1acf91894b13fb46fedfd179ea7f88c8"


# def test_category_delete_version(test_client, authentication_headers):
#     """Delete specific version of category."""
#     response = test_client.delete('/api/v1/categories/categoryname/version/0.0.1', headers=authentication_headers)
#     assert response.status_code == 204
