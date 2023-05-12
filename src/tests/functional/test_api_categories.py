import json

def test_get_category_not_exist(test_client, authentication_headers):
    """Check that it shows a proper 404 category not found message when a non-existing category is requested."""
    response = test_client.get('/api/v1/categories/idonotexist', headers=authentication_headers)
    assert response.status_code == 404
    assert response.json == {"error": "Category not found."}


def test_create_category_wrong_post_data(test_client, authentication_headers):
    """Check that we get a 400 when we POST data with a not accepting key name."""
    postdict = {
        "names": "categoryname"
    }
    response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 400
    assert data["errors"][""] == "Additional properties are not allowed ('names' was unexpected)"


def test_create_category_unauthenticated(test_client):
    """Check that we need to provide authentication details when we want to create a new catagory."""
    postdict = {
        "name": "categoryname"
    }
    response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

    data = response.json
    assert response.status_code == 401


def test_create_category(test_client, authentication_headers):
    """Check that we get the proper information when we are authenticated and create a new catagory."""
    postdict = {
        "name": "categoryname"
    }
    response = test_client.post('/api/v1/categories', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['name'] == "categoryname"
    assert data['created_by'] == "admin"


def test_delete_category_not_exist(test_client, authentication_headers):
    """Check if we get a 404 when we want to delete a catagory that doesn't exist."""
    response = test_client.delete('/api/v1/categories/idonotexist', headers=authentication_headers)
    assert response.status_code == 404
    assert response.json == {"error": "Category not found."}


def test_delete_category(test_client, authentication_headers):
    """Check if we get a 204 when we want to delete a catagory."""
    response = test_client.delete('/api/v1/categories/categoryname', headers=authentication_headers)
    assert response.status_code == 204
    assert response.text == ""
