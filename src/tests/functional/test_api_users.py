# import json


# def test_api_users_login_correct(test_client):
#     """
#     Use a correct username/password combination to validate authentication.
#     """
#     postdict = {
#         "username": "admin",
#         "password": "password"
#     }
#     response = test_client.post('/api/v1/users/authenticate', data=json.dumps(postdict), headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 200
#     assert "token" in data


# def test_api_users_login_incorrect(test_client):
#     """
#     Use an incorrect username/password combination to validate authentication error message.
#     """
#     postdict = {
#         "username": "somenotexistinguser",
#         "password": "password"
#     }
#     response = test_client.post('/api/v1/users/authenticate', data=json.dumps(postdict), headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 401
#     assert "error" in data
#     assert data['error'] == "Authentication failed. Invalid username/password combination"



# def test_api_users_login_incorrect_dict(test_client):
#     """
#     Provide a wrong data to authenticate.
#     """
#     postdict = {
#         "usernamee": "admin",
#         "passwrd": "password"
#     }
#     response = test_client.post('/api/v1/users/authenticate', data=json.dumps(postdict), headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 400
#     assert "message" in data
#     assert data['message'] == "Input payload validation failed"



# def test_api_users_register_user_already_exist(test_client):
#     """
#     Register a new user that already exist.
#     """
#     postdict = {
#         "username": "admin",
#         "password": "password",
#         "groups": ["admin"]
#     }
#     response = test_client.post('/api/v1/users/register', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 409
#     assert data['error'] == "Username is already used."


# def test_api_users_register_new_user(test_client, getRandomName):
#     """
#     Register a complete new user in an existing group.
#     """
#     postdict = {
#         "username": getRandomName,
#         "password": "password",
#         "groups": ["admin"]
#     }
#     response = test_client.post('/api/v1/users/register', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data["username"] == getRandomName
#     assert "admin" in data["groups"]
#     assert data['is_active']
    

# def test_api_users_register_new_user_not_existing_group(test_client, getRandomName):
#     """
#     Register a complete new user in a not-existing group.
#     """
#     postdict = {
#         "username": getRandomName,
#         "password": "password",
#         "groups": ["admin1"]
#     }
#     response = test_client.post('/api/v1/users/register', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 409
#     assert data['error'] == "The groups ['admin1'] doesn't exist"


# def test_api_users_register_and_auth_new_inactive_user(test_client, getRandomName):
#     """
#     Register an in_active (false) user and try to authenticate with.
#     """
#     postdict = {
#         "is_active": False,
#         "username": getRandomName,
#         "password": "password",
#         "groups": ["admin"]
#     }
#     response = test_client.post('/api/v1/users/register', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 201
#     assert data["username"] == getRandomName
#     assert "admin" in data["groups"]
#     assert not data['is_active']

#     postdict = {
#         "username": getRandomName,
#         "password": "password"
#     }
#     response = test_client.post('/api/v1/users/authenticate', data=json.dumps(postdict), headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 401
#     assert "error" in data
#     assert data['error'] == "Authentication failed. Invalid username/password combination"
