from tests.conftest import USER_NAME, USER_EMAIL, USER_PASSWORD, user

def test_create_user(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert "password" not in response.json()
    

def test_create_user_with_existing_email(client, inactive_user):
    
    '''
    ********** one way to do it ****

    # Create a dictionary representing a new user
    existing_user = {
    "name": "Existing User",  # User's name
    "email": "existing_user@example.com",  # User's email
    "password": USER_PASSWORD   # User's password
    }

    # Attempt to create the existing user via the API
    response = client.post('/users', json=existing_user)
    assert response.status_code == 201  # Check that the user was created successfully

    # Prepare data for another user with the same email
    data = {
    "name": "Hasnain Hasib",  # New user's name
    "email": existing_user["email"],  # Same email as the existing user
    "password": USER_PASSWORD  # New user's password
    }

    ********* and this one using fixture for reusable test data ************************
    '''
    data = {
        "name": "Hasnain Hasib",
        "email": user.email,  # Same email as existing user
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code == 400  # Should return a 400 error
    assert response.json()["detail"] == "Email already exists."


def test_create_user_with_invalid_email(client):
    data = {
        "name": "Hasnain Hasib",
        "email": "keshari.com",
        "password": USER_PASSWORD
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_empty_password(client):
    data = {
        "name": "Hasnain Hasib",
        "email": USER_EMAIL,
        "password": ""
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_numeric_password(client):
    data = {
        "name": "Hasnain Hasib",
        "email": USER_EMAIL,
        "password": "1232382318763"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_char_password(client):
    data = {
        "name": "Hasnain Hasib",
        "email": USER_EMAIL,
        "password": "asjhgahAdF"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_alphanumeric_password(client):
    data = {
        "name": "Hasnain Hasib",
        "email": USER_EMAIL,
        "password": "sjdgajhGG27862"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201