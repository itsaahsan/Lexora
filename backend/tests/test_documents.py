import io


def test_upload_document(client, auth_headers):
    file_content = b"This is a test document content."
    response = client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["file_type"] == "txt"


def test_upload_invalid_type(client, auth_headers):
    response = client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("test.exe", io.BytesIO(b"bad"), "application/octet-stream")},
    )
    assert response.status_code == 400


def test_list_documents(client, auth_headers):
    client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", io.BytesIO(b"content"), "text/plain")},
    )
    response = client.get("/api/documents", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_delete_document(client, auth_headers):
    upload = client.post(
        "/api/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", io.BytesIO(b"content"), "text/plain")},
    )
    doc_id = upload.json()["id"]
    response = client.delete(f"/api/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200


def test_unauthorized_upload(client):
    response = client.post(
        "/api/documents/upload",
        files={"file": ("test.txt", io.BytesIO(b"content"), "text/plain")},
    )
    assert response.status_code == 401
