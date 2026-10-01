def test_create_user(client):
    response = client.post(
        "/v1/users/",
        json={
            "name": "Lucas",
            "email": "lucas@email.com",
            "password": "123456",
            "password_confirmation": "123456",
            "address": "Rua X",
            "phone": "77999999999",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Lucas"
    assert data["email"] == "lucas@email.com"
    assert "hashed_password" not in data
    assert "password" not in data


def test_create_user_with_duplicated_email(client):
    payload = {
        "name": "Lucas",
        "email": "lucas@email.com",
        "password": "123456",
        "password_confirmation": "123456",
        "address": "Rua X",
        "phone": "77999999999",
    }

    client.post("/v1/users/", json=payload)

    response = client.post(
        "/v1/users/",
        json={
            **payload,
            "phone": "77888888888",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_login(client):
    client.post(
        "/v1/users/",
        json={
            "name": "Lucas",
            "email": "lucas@email.com",
            "password": "123456",
            "password_confirmation": "123456",
            "address": "Rua X",
            "phone": "77999999999",
        },
    )

    response = client.post(
        "/v1/auth/login",
        json={
            "email": "lucas@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_with_wrong_password(client):
    client.post(
        "/v1/users/",
        json={
            "name": "Lucas",
            "email": "lucas@email.com",
            "password": "123456",
            "password_confirmation": "123456",
            "address": "Rua X",
            "phone": "77999999999",
        },
    )

    response = client.post(
        "/v1/auth/login",
        json={
            "email": "lucas@email.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_list_users_requires_token(client):
    response = client.get("/v1/users/")

    assert response.status_code == 401


def test_list_users_with_valid_token(client):
    client.post(
        "/v1/users/",
        json={
            "name": "Lucas",
            "email": "lucas@email.com",
            "password": "123456",
            "password_confirmation": "123456",
            "address": "Rua X",
            "phone": "77999999999",
        },
    )

    login_response = client.post(
        "/v1/auth/login",
        json={
            "email": "lucas@email.com",
            "password": "123456",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/v1/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "pagination" in data