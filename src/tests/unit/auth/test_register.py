import uuid

# def test_register(client, freezer, jwt_auth):
#     freezer.move_to("2023-01-11 00:00:00")
#     response = client.post(
#         "/api/v1/auth/register",
#         data={"username": "tester123", "password": "tester321"},
#     )
#     assert response.status_code == 201
#     assert list(response.json().keys()) == ["access_token", "refresh_token"]
#     assert jwt_auth.decode_token(response.json().get("access_token")) == {
#         "iss": "http://localhost:8000",
#         "sub": "tester123",
#         "type": "access",
#         "jti": "b3a8d4a1-6f2a-4e9c-8c9e-6d8e9a3b6c6d",
#         "iat": 1672905600,
#         "nbf": 1672905600,
#         "exp": 1672909200,
#     }


def test_generate_access_token(freezer, jwt_auth):
    freezer.move_to("2023-01-11 00:00:00")
    device_id = str(uuid.uuid4())
    subject = "tester123"
    token = jwt_auth.generate_access_token(subject, {"device_id": device_id})
    decoded_token = jwt_auth.decode_token(token)
    assert decoded_token["iss"] == "FastAPI"
    assert decoded_token["sub"] == subject
    assert decoded_token["type"] == "ACCESS"
    assert decoded_token["iat"] == 1673395200
    assert decoded_token["nbf"] == 1673395200
    assert decoded_token["exp"] == 1673398800
