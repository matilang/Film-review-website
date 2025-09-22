import pytest
## CRUD testing reviews


def test_add_review(client, sample_film):
    film_id = sample_film['id']    
    review = "Very nice film"
    rating = 2.3

    response = client.post(
        f"/films/{film_id}/reviews/", 
        json={"film_id" : film_id, "review_text" : review, "rating" : rating}
        )
        
    assert response.status_code == 201
    assert response.json()['film_id'] == film_id
    assert response.json()['review_text'] == review
    assert response.json()['rating'] == rating
    
def test_get_all_reviews(client, sample_film, sample_list_of_reviews):
    film_id = sample_film['id']
    response = client.get(f"/films/{film_id}/reviews/")
    assert response.status_code == 200
    
    reviews = response.json()
    assert len(reviews) == len(sample_list_of_reviews)
    assert all(r['film_id'] == film_id for r in reviews)

def test_get_rating_average(client, sample_film, sample_list_of_reviews):
    film_id = sample_film['id']
    
    response = client.get(f"/films/{film_id}/rating")
    assert response.status_code == 200
        
    sample_rating = sum(r['rating'] for r in sample_list_of_reviews) / len(sample_list_of_reviews)
    assert float(response.json()) == pytest.approx(sample_rating, rel=1e-2)