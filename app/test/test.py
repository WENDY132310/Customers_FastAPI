from fastapi.testclient import TestClient

def test_client(client):
    assert type (client)== TestClient    # assert permite validar valores iguales