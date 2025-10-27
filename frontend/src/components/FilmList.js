import FilmCard from "./FilmCard";
import { useState, useEffect } from "react"

export default function FilmList (){
    const [films, setFilms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/films/")
            .then((response) => {
                if(!response.ok) {
                    throw new Error("Błąd sieci")
                }
                return response.json()
            })
            .then((data) => {
                setFilms(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [])

    if(loading) return <p>Ładowanie...</p>
    if(error) return <p>Błąd: {error}</p>

    return(
        <div className="film-list">
            {films.map(film =>
                <div key={film.id}>
                   <FilmCard {...film} /> 
                </div>
            )}
        </div>
    )




}
