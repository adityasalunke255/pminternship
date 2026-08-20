import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="skeleton-grid">
      {[1, 2, 3].map((item) => (
        <div key={item} className="skeleton-card">
          <div className="skeleton-line w-60 h-lg"></div>
          <div className="skeleton-line w-40" style={{ marginBottom: '24px' }}></div>
          <div className="skeleton-line"></div>
          <div className="skeleton-line w-80"></div>
          <div className="skeleton-line w-50" style={{ marginBottom: '24px' }}></div>
          <div className="skeleton-line h-btn"></div>
        </div>
      ))}
    </div>
  );
};

export default LoadingSpinner;
