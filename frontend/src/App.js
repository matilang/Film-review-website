import { Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import FilmPage from './pages/FilmPage';

export default function App() {
  return(
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/films/:filmId' element={<FilmPage/>}/>
      </Routes>
  );
}

