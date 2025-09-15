## CRUD testing books


def test_get_list_of_books(client, sample_list_of_books):    
    response = client.get("/books/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(sample_list_of_books)
    
    for book in data:
        assert "title" in book
        assert "author" in book
        assert "year" in book

def test_get_list_of_books_with_limits(client, sample_list_of_books):    
    response = client.get("/books/?offset=1")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_list_of_books)-1
    
    response = client.get("/books/?author=Author C")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_list_of_books)-2
    
    response = client.get("/books/?year=2000")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_list_of_books)-2
    
    response = client.get("/books/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_list_of_books)-2

def test_create_book(client):
    
    book = {"title" : "Book A", "author" : "Author A", "year" : 2000}
    response = client.post("/books/", json=book)
    assert response.status_code == 201
    
    assert response.json()['title'] == book['title']
    assert response.json()['author'] == book['author']
    assert response.json()['year'] == book["year"]
    assert 'id' in response.json()

def test_get_book_by_id(client, sample_list_of_books):
    book_id = sample_list_of_books[0]['id']
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()['id'] == book_id
    assert response.json()['title'] == sample_list_of_books[0]['title']
    
def test_update_book(client, sample_book):
    book_id = sample_book['id']
    original_book_title = sample_book["title"]
    
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()['id'] == book_id
    assert response.json()['title'] == original_book_title
    
    new_book_title = "New Book"
    response = client.patch(f"/books/{book_id}", json={"title" : new_book_title})
    assert response.status_code == 200
    assert response.json()['title'] == new_book_title
    assert response.json()['id'] == book_id

def test_delete_book(client, sample_book):
    book_id = sample_book['id']
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    
    response = client.delete(f"books/{book_id}")
    assert response.status_code == 200
    
    response = client.get(f"books/{book_id}")
    assert response.status_code == 404
    