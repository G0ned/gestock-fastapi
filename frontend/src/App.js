import './App.css';
// Routes agrupa las rutas y Route asocia una URL con el componente que se debe mostrar
import { Routes, Route } from 'react-router-dom';
import LandingSection from './components/LandingSection';
import Header from './components/Header';
import ProductsPage from './pages/ProductsPage';

function App() {
  return (
    <main>
      {/* El header queda fuera de Routes para que se vea en todas las páginas */}
      <Header />
      {/* Solo se renderiza la Route cuyo path coincide con la URL actual */}
      <Routes>
        <Route path="/" element={<LandingSection />} />
        <Route path="/products" element={<ProductsPage />} />
      </Routes>
    </main>
  );
}

export default App;
