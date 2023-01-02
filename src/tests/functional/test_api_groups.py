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


# def test_api_groups_add_user_to_group_no_auth(test_client):
#     """
#     Create a new group and do a get to validate that it exist.
#     """
#     headers={'Content-Type': "application/json"}
#     response = test_client.post('/api/v1/groups/newgroup/user/admin', data=json.dumps({}), headers=headers)
#     data = response.json
#     assert response.status_code == 401
#     assert data["msg"] == "Missing Authorization Header"


# def test_api_groups_add_user_to_group(test_client, authentication_headers):
#     """
#     Create a new group and do a get to validate that it exist.
#     """

#     responsePost = test_client.post('/api/v1/groups/newgroup/user/admin', data=json.dumps({}), headers=authentication_headers)
#     dataPost = responsePost.json
#     responseGet = test_client.get('/api/v1/groups/newgroup', headers=authentication_headers)
#     dataGet = responseGet.json

#     assert responsePost.status_code == 201
#     assert dataGet["name"] == "newgroup"
#     assert len(dataGet["users"]) == 1
#     assert responseGet.status_code == 200
#     assert dataPost["message"] == "User added to group."


# def test_api_groups_add_non_exiting_user_to_group(test_client, authentication_headers):
#     """
#     Create a new group and do a get to validate that it exist.
#     """

#     responsePost = test_client.post('/api/v1/groups/newgroup/user/notexist', data=json.dumps({}), headers=authentication_headers)
#     dataPost = responsePost.json
#     responseGet = test_client.get('/api/v1/groups/newgroup', headers=authentication_headers)
#     dataGet = responseGet.json

#     assert responsePost.status_code == 404
#     assert dataGet["name"] == "newgroup"
#     assert len(dataGet["users"]) == 1
#     assert responseGet.status_code == 200
#     assert dataPost["error"] == "Username and/or group not found."


# def test_api_groups_delete_user_from_group(test_client, authentication_headers):
#     """
#     Create a new group and do a get to validate that it exist.
#     """

#     responseDelete = test_client.delete('/api/v1/groups/newgroup/user/admin', headers=authentication_headers)
#     dataDelete = responseDelete.text
#     responseGet = test_client.get('/api/v1/groups/newgroup', headers=authentication_headers)
#     dataGet = responseGet.json

#     assert responseDelete.status_code == 204
#     assert dataGet["name"] == "newgroup"
#     assert len(dataGet["users"]) == 0
#     assert responseGet.status_code == 200
#     assert dataDelete == ""


# # Why is this one showing a 404 when this is not authenticated?
# # def test_api_groups_delete_group_no_auth(test_client):
# #     """
# #     Create a new group and do a get to validate that it exist.
# #     """
# #     headers={'Content-Type': "application/json"}
# #     response = test_client.delete('/api/v1/groups/pizza', headers=headers)
# #     data = response.json
# #     assert response.status_code == 401
# #     assert data["msg"] == "Missing Authorization Header"


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


# def test_api_groups_delete_group_removing_added_user(test_client, authentication_headers, getRandomName):
#     """
#     Create new group and user and then delete the group, group entry should also be removed in user output.
#     """
#     username = getRandomName
#     username_url = '/api/v1/users/{u}'.format(u=username)
#     postdict = {
#         "name": "newgroup"
#     }
#     postUserdict = {
#         "username": username,
#         "password": "password",
#         "groups": ["admin", "newgroup"]
#     }
#     test_client.post('/api/v1/groups/', data=json.dumps(postdict), headers=authentication_headers)
#     responseCreate = test_client.post('/api/v1/users/register', data=json.dumps(postUserdict), headers={'Content-Type': "application/json"}, follow_redirects=True)
#     dataCreate = responseCreate.json

#     test_client.delete('/api/v1/groups/newgroup', headers=authentication_headers, follow_redirects=True)
#     responseGet = test_client.get(username_url, headers=authentication_headers)
#     dataGet = responseGet.json

#     assert 'newgroup' in dataCreate["groups"]
#     assert 'newgroup' not in dataGet["groups"]
#     assert responseGet.status_code == 200
