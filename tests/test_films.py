## CRUD testing films


def test_get_list_of_films(client, sample_list_of_films):    
    response = client.get("/films/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(sample_list_of_films)
    
    for film in data:
        assert "title" in film
        assert "director" in film
        assert "year" in film

def test_get_list_of_films_with_limits(client, sample_list_of_films):   
    # paginate 
    response = client.get("/films/?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    response = client.get("/films/?director=Director C")
    assert response.status_code == 200
    assert len(response.json()) == 4
    
    response = client.get("/films/?year=2000")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    response = client.get("/films/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_create_film(client):
    
    film = {"title" : "Film A", "director" : "Director A", "year" : 2000}
    response = client.post("/films/", json=film)

    assert response.status_code == 201
    assert response.json()['title'] == film['title']
    assert response.json()['director'] == film['director']
    assert response.json()['year'] == film["year"]
    assert 'id' in response.json()
    
def test_create_film_with_missing_data(client):
    # no title
    response = client.post("/films/", json={"director" : "Director A", "year" : 2000})
    assert response.status_code == 422
    
    # no director
    response = client.post("/films/", json={"title" : "Film A", "year" : 2000})
    assert response.status_code == 422

def test_get_film_by_id(client, sample_list_of_films):
    film_id = sample_list_of_films[0]['id']
    response = client.get(f"/films/{film_id}")

    assert response.status_code == 200
    assert response.json()['id'] == film_id
    assert response.json()['title'] == sample_list_of_films[0]['title']
    
def test_get_film_by_wrong_id(client, sample_list_of_films):
    film_list_length = len(sample_list_of_films)
    film_id = sample_list_of_films[0]['id'] + film_list_length + 1
    response = client.get(f"/films/{film_id}")

    assert response.status_code == 404
    
def test_update_film(client, sample_film):
    film_id = sample_film['id']
    original_film_title = sample_film["title"]
    
    response = client.get(f"/films/{film_id}")
    assert response.status_code == 200
    assert response.json()['id'] == film_id
    assert response.json()['title'] == original_film_title
    
    new_film_title = "New Film"
    response = client.patch(f"/films/{film_id}", json={"title" : new_film_title})
    assert response.status_code == 200
    assert response.json()['title'] == new_film_title
    assert response.json()['id'] == film_id
    
def test_update_nonexistent_film(client, sample_film):
    film_id = sample_film['id']
    
    new_film_title = "New Film"
    wrong_id = film_id + 1
    response = client.patch(f"/films/{wrong_id}", json={"title" : new_film_title})
    assert response.status_code == 404

def test_delete_film(client, sample_film):
    film_id = sample_film['id']
    response = client.get(f"/films/{film_id}")
    assert response.status_code == 200
    
    response = client.delete(f"films/{film_id}")
    assert response.status_code == 200
    
    response = client.get(f"films/{film_id}")
    assert response.status_code == 404
    
def test_delete_nonexistent_film(client, sample_film):
    film_id = sample_film['id']
    
    wrong_id = film_id + 1
    response = client.delete(f"films/{wrong_id}")
    assert response.status_code == 404
    
