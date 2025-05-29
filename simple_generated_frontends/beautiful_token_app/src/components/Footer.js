import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">
              © 2024 All rights reserved
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm">Powered by Aleo</span>
            <span className="text-sm text-gray-400">•</span>
            <span className="text-sm font-semibold">Made with AleoForge</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;