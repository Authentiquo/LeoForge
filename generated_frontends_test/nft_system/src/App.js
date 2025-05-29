import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import TokenOperations from './pages/TokenOperations';
import AdminOperations from './pages/AdminOperations';
import NftOperations from './pages/NftOperations';
import Dashboard from './pages/Dashboard';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
          <Route path="/token" element={<TokenOperations />} />
          <Route path="/admin" element={<AdminOperations />} />
          <Route path="/nft" element={<NftOperations />} />
          <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;