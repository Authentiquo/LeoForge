import React, { useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

const PublicOperations = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e, transitionName) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setResult({
        success: true,
        message: `${transitionName} executed successfully!`,
        txId: `0x${Math.random().toString(16).substr(2, 8)}`
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Public Operations</h1>
        <p className="mt-2 text-gray-600">
          Manage public operations on the Aleo blockchain
        </p>
      </div>

      {/* Result Display */}
      {result && (
        <div className={`p-4 rounded-lg ${result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
          <p className={`font-semibold ${result.success ? 'text-green-800' : 'text-red-800'}`}>
            {result.message}
          </p>
          {result.txId && (
            <p className="text-sm text-gray-600 mt-1">
              Transaction ID: {result.txId}
            </p>
          )}
        </div>
      )}

      {/* Forms */}
      <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            Transfer Public
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'transfer_public')} className="space-y-4">
            <p className="text-gray-600">This function requires private parameters</p>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <ArrowPathIcon className="animate-spin h-5 w-5 mr-2" />
                  Processing...
                </span>
              ) : (
                'Execute'
              )}
            </button>
          </form>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            Private To Public
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'private_to_public')} className="space-y-4">
            <p className="text-gray-600">This function requires private parameters</p>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <ArrowPathIcon className="animate-spin h-5 w-5 mr-2" />
                  Processing...
                </span>
              ) : (
                'Execute'
              )}
            </button>
          </form>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">
            Public To Private
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'public_to_private')} className="space-y-4">
            <p className="text-gray-600">This function requires private parameters</p>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-aleo-blue text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <ArrowPathIcon className="animate-spin h-5 w-5 mr-2" />
                  Processing...
                </span>
              ) : (
                'Execute'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PublicOperations;