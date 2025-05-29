import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-aleo-blue rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              Amine Token
            </span>
          </Link>
          
          <div className="flex space-x-6">
            <Link
              to="/token"
              className="text-gray-700 hover:text-aleo-blue transition-colors"
            >
              Token Operations
            </Link>
            <Link
              to="/public"
              className="text-gray-700 hover:text-aleo-blue transition-colors"
            >
              Public Operations
            </Link>
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-aleo-blue transition-colors"
            >
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;