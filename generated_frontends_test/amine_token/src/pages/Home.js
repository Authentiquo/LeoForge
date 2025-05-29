import React from 'react';
import { Link } from 'react-router-dom';
import { CubeTransparentIcon, CircleStackIcon, CodeBracketIcon } from '@heroicons/react/24/outline';

const Home = () => {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Amine Token
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          A powerful Aleo smart contract interface for decentralized operations
        </p>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <CubeTransparentIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Smart Contract</h3>
          <p className="text-gray-600">
            Built on Aleo blockchain with privacy-preserving technology
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <CircleStackIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Data Storage</h3>
          <p className="text-gray-600">
            2 mappings and 1 record types
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <CodeBracketIcon className="h-12 w-12 text-aleo-blue mb-4" />
          <h3 className="text-xl font-semibold mb-2">Functions</h3>
          <p className="text-gray-600">
            7 transitions available
          </p>
        </div>
      </section>

      {/* Contract Info */}
      <section className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold mb-6">Contract Overview</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-3">Available Operations</h3>
            <ul className="space-y-2 text-gray-600">
              <li className="flex items-center space-x-2"><span className="text-aleo-blue">•</span><span>Mint</span></li>
              <li className="flex items-center space-x-2"><span className="text-aleo-blue">•</span><span>Transfer Public</span></li>
              <li className="flex items-center space-x-2"><span className="text-aleo-blue">•</span><span>Private To Public</span></li>
              <li className="flex items-center space-x-2"><span className="text-aleo-blue">•</span><span>Public To Private</span></li>
              <li className="flex items-center space-x-2"><span className="text-aleo-blue">•</span><span>Burn Public</span></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-3">Contract Stats</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Transitions:</span>
                <span className="font-semibold">7</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Mappings:</span>
                <span className="font-semibold">2</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Records:</span>
                <span className="font-semibold">1</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Constants:</span>
                <span className="font-semibold">2</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="text-center py-8">
        <Link
          to="/dashboard"
          className="inline-block bg-aleo-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Get Started
        </Link>
      </section>
    </div>
  );
};

export default Home;