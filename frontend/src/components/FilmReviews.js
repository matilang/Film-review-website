import { useState, useEffect } from "react";


export default function FilmReviews ({filmId}) {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`http://127.0.0.1:8000/films/${filmId}/reviews`, { signal: controller.signal });
                if(!response.ok) {
                    throw new Error("Network error" );
                }
                const data = await response.json();
                setReviews(data);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message || 'Loading error');
                }
            } finally {
                setLoading(false);
            }
        }

        load();
        return () => controller.abort();
    }, [filmId])

    if(loading) return <p>Loading...</p>
    if(error) return (
        <div>
            <p>Błąd: {error}</p>
            <button onClick={() => window.location.reload()}>Try again</button>
        </div>
    )

    if(!loading && reviews.length === 0) return (
        <div>
            <p>No reviews</p>
        </div>
    )

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