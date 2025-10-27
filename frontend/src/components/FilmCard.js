
export default function FilmCard ( {title, director, year} ) {
    return (
        <div className='film-card'>
            <h2>{title}</h2>
            <p>Director : {director}</p>
            <p>Year : {year}</p>
        </div>
    );
}