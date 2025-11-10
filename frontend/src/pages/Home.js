import FilmList from "../components/FilmList";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function Home () {
    return(
        <div>
            <Navbar/>
            <FilmList/>
            <Footer/>
        </div>
    );
}