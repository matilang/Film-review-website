import { useState, useEffect } from "react";


export default function FilmReviews ({filmId}) {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/films/${filmId}/reviews`)
            .then((response) => {
                if(!response.ok) {
                    throw new Error("Błąd sieci")
                }
                return response.json()
            })
            .then((data) => {
                setReviews(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [filmId])

    if(loading) return <p>Ładowanie...</p>
    if(error) return <p>Błąd: {error}</p>

    return(
        <div className="review-list">
            {reviews.map(review => 
                <div key={review.id}>
                    <ReviewBox 
                    userName={review.user_id}
                    reviewText={review.review_text}
                    rating={review.rating}/>
                </div>
            )}
        </div>
    )
}

function ReviewBox ({userName, reviewText, rating}){
    return(
        <div className="review-box">
            <h3>Author: {userName}</h3>
            <p>{reviewText}</p>
            <p>Rating: {rating}</p>
        </div>
    )
}