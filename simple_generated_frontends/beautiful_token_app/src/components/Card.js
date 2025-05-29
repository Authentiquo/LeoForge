import React from 'react';

const Card = ({ children, className = '' }) => {
  return (
    <div className={`bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 ${className}`}>
      {children}
    </div>
  );
};

export default Card;