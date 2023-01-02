
# def test_get_bom_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/bom/all', headers={'Content-Type': "application/json"}, follow_redirects=True)
#     assert response.status_code == 401


# def test_get_bom(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/bom/all', headers=authentication_headers, follow_redirects=True)
#     data = response.json
#     assert response.status_code == 200
#     assert 'mygroup' in data
#     assert 'artifactname' in data['mygroup']
#     assert data['mygroup']['artifactname'] == "1.0.1"


# def test_get_bom_group_not_exist_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/bom/group/notexistinggroup', headers={'Content-Type': "application/json"}, follow_redirects=True)
#     assert response.status_code == 401


# def test_get_bom_group_not_exist(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/bom/group/notexistinggroup', headers=authentication_headers, follow_redirects=True)
#     data = response.json
#     assert response.status_code == 404
#     assert data['message'] == "Group not found."

# def test_get_bom_group_exist(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/bom//group/mygroup', headers=authentication_headers, follow_redirects=True)
#     data = response.json
#     assert response.status_code == 200
#     assert 'mygroup' in data
#     assert 'artifactname' in data['mygroup']
#     assert data['mygroup']['artifactname'] == "1.0.1"
