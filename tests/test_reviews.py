import pytest
## CRUD testing reviews


def test_add_review(client, sample_book):
    book_id = sample_book['id']    
    review = "Very nice book"
    rating = 2.3

    response = client.post(
        f"/books/{book_id}/reviews/", 
        json={"book_id" : book_id, "review_text" : review, "rating" : rating}
        )
        
    assert response.status_code == 201
    assert response.json()['book_id'] == book_id
    assert response.json()['review_text'] == review
    assert response.json()['rating'] == rating
    
def test_get_all_reviews(client, sample_book, sample_list_of_reviews):
    book_id = sample_book['id']
    response = client.get(f"/books/{book_id}/reviews/")
    assert response.status_code == 200
    
    reviews = response.json()
    assert len(reviews) == len(sample_list_of_reviews)
    assert all(r['book_id'] == book_id for r in reviews)

def test_get_rating_average(client, sample_book, sample_list_of_reviews):
    book_id = sample_book['id']
    
    response = client.get(f"/books/{book_id}/rating")
    assert response.status_code == 200
        
    sample_rating = sum(r['rating'] for r in sample_list_of_reviews) / len(sample_list_of_reviews)
    assert float(response.json()) == pytest.approx(sample_rating, rel=1e-2)