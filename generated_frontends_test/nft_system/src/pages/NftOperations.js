import React, { useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

const NftOperations = () => {
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
        <h1 className="text-3xl font-bold text-gray-900">Nft Operations</h1>
        <p className="mt-2 text-gray-600">
          Manage nft operations on the Aleo blockchain
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
            Mint Nft
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'mint_nft')} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              To
            </label>
            <input
              type="text"
              name="to"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter to"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Metadata Hash
            </label>
            <input
              type="text"
              name="metadata_hash"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter metadata hash"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Rarity
            </label>
            <input
              type="number"
              name="rarity"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter rarity"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Collection Id
            </label>
            <input
              type="number"
              name="collection_id"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter collection id"
            />
          </div>
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
            Claim Random Nft
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'claim_random_nft')} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Additional Entropy
            </label>
            <input
              type="text"
              name="additional_entropy"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter additional entropy"
            />
          </div>
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
            Transfer Nft Public
          </h2>
          <form onSubmit={(e) => handleSubmit(e, 'transfer_nft_public')} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nft Id
            </label>
            <input
              type="number"
              name="nft_id"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter nft id"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              To
            </label>
            <input
              type="text"
              name="to"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aleo-blue"
              placeholder="Enter to"
            />
          </div>
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

export default NftOperations;