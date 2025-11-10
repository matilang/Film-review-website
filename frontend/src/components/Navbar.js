import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="navbar">
            <h1>Film Library</h1>
            <button>
                <Link to="/">Home</Link>
            </button>
        </nav>
    );
}