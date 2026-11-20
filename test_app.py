from app import app

def test_home_status_code():
    client = app.test_client()
    assert client.get("/").status_code == 200

def test_home_response_body():
    client = app.test_client()
    assert client.get("/").data.decode() == "Hello, CI/CD!"
