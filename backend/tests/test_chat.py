def test_list_conversations(client, auth_headers):
    response = client.get("/api/conversations", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_conversation_unauthorized(client):
    response = client.get("/api/conversations")
    assert response.status_code == 401


def test_delete_nonexistent_conversation(client, auth_headers):
    response = client.delete("/api/conversations/nonexistent", headers=auth_headers)
    assert response.status_code == 404
