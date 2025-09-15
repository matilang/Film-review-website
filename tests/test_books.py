## Book CRUD testing


def test_create_book(client, sample_book):
    response = client.get(f"/books/{sample_book['id']}")
    assert response.status_code == 200
    
