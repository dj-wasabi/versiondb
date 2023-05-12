# import json


# def test_api_groups_create_group_no_auth(test_client):
#     """
#     Create a new group and do a get to validate that it exist.
#     """
#     headers={'Content-Type': "application/json"}
#     postdict = {
#         "name": "newgroup"
#     }
#     response = test_client.post('/api/v1/groups/', data=json.dumps(postdict), headers=headers)

#     data = response.json
#     assert response.status_code == 401
#     assert data["msg"] == "Missing Authorization Header"


# def test_api_groups_create_group(test_client, authentication_headers):
#     """
#     Create a new group and do a get to validate that it exist.
#     """
#     postdict = {
#         "name": "newgroup"
#     }
#     response = test_client.post('/api/v1/groups/', data=json.dumps(postdict), headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 201
#     assert data["name"] == "newgroup"
#     assert len(data["users"]) == 0

#     response = test_client.get('/api/v1/groups/newgroup', headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 200
#     assert data["name"] == "newgroup"
#     assert len(data["users"]) == 0


# def test_api_groups_delete_group_no_auth(test_client):
#     """
#     Create a new group and do a get to validate that it exist.
#     """
#     headers={'Content-Type': "application/json"}
#     response = test_client.delete('/api/v1/groups/pizza', headers=headers)
#     data = response.json
#     assert response.status_code == 401
#     assert data["msg"] == "Missing Authorization Header"


# def test_api_groups_get_group_not_exist(test_client, authentication_headers):
#     """
#     Delete a non-existing group.
#     """
#     response = test_client.get('/api/v1/groups/newgroupno', headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 404
#     assert data["error"] == "Group not found."


# def test_api_groups_delete_group(test_client, authentication_headers):
#     """
#     Delete a group and validate that it is removed.
#     """
#     response = test_client.delete('/api/v1/groups/newgroup', headers=authentication_headers)

#     data = response.text
#     assert response.status_code == 204
#     assert data == ""


#     response = test_client.delete('/api/v1/groups/newgroup', headers=authentication_headers)

#     data = response.json
#     assert response.status_code == 404
#     assert data["error"] == "Group not found."
