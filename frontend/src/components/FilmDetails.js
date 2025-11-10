import FilmCard from "../components/FilmCard";
import FilmReviews from "../components/FilmReviews";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function FilmDetails () {
    const {filmId} = useParams();
    const [film, setFilm] = useState();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/films/${filmId}`)
            .then((response) => {
                if(!response.ok) {
                    throw new Error("Network Error")
                }
                return response.json()
            })
            .then((data) => {
                setFilm(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [filmId])

    if(loading) return <p>Loading...</p>
    if(error) return <p>Error: {error}</p>

    return(
        <div className="film-page">
            <FilmCard 
            title={film.title}
            director={film.director}
            year={film.year}/>
            <FilmReviews filmId={filmId}/>
        </div>
    )
}