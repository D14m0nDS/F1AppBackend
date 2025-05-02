import pytest

def test_ping(client):
    resp = client.get("/test/ping")
    assert resp.status_code == 200
    assert resp.json == {"message": "Pong!"}

def test_echo_success(client):
    payload = {"foo": "bar", "baz": 123}
    resp = client.post("/test/echo", json=payload)
    assert resp.status_code == 200
    assert resp.json == {"echoed_data": payload}

def test_echo_no_json(client):
    resp = client.post("/test/echo")
    assert resp.status_code == 400
    assert resp.json["error"] == "No JSON data provided"

def test_secure_ping_requires_token(client):
    resp = client.get("/test/secure-ping")
    assert resp.status_code == 401

def test_secure_ping_with_token(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = client.get("/test/secure-ping", headers=headers)
    assert resp.status_code == 200
    assert resp.json == {"message": "Pong from a secure endpoint!"}

@pytest.mark.parametrize("param", ["hello", "123", "with-dashes"])
def test_params(client, param):
    resp = client.get(f"/test/params/{param}")
    assert resp.status_code == 200
    assert resp.json == {"received_param": param}
