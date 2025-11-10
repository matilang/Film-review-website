import { Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import FilmDetails from './components/FilmDetails';

export default function App() {
  return(
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/films/:filmId' element={<FilmDetails/>}/>
      </Routes>
  );
}

