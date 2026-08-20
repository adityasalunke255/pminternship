import React, { useState } from 'react';
import Header from './components/Header';
import CandidateForm from './components/CandidateForm';
import RecommendationCard from './components/RecommendationCard';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [tier1, setTier1] = useState([]);
  const [tier2, setTier2] = useState([]);
  const [tier3, setTier3] = useState([]);
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const fetchRecommendations = async (formData) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    
    setTier1([]);
    setTier2([]);
    setTier3([]);

    try {
      const response = await fetch('/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      
      setTier1(data.tier_1 || []);
      setTier2(data.tier_2 || []);
      setTier3(data.tier_3 || []);
      
    } catch (err) {
      console.error(err);
      setError('Something went wrong. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Header />
      <main className="main-container">
        
        <section className="hero-section">
          <h2 className="hero-title">
            Internship Matching Portal
          </h2>
          <p className="hero-subtitle">
            Provide your qualifications and skills to discover suitable opportunities from the PM Internship Scheme.
          </p>
        </section>

        <CandidateForm onSubmit={fetchRecommendations} isLoading={isLoading} />

        {hasSearched && (
          <section className="results-section" id="results">
            {error && <div className="error-message" style={{color: 'red', textAlign: 'center'}}>{error}</div>}

            {isLoading && <LoadingSpinner />}

            {!isLoading && !error && (
              <>
                {/* TIER 1 - Perfect Matches */}
                <div className="tier-section">
                  <div className="tier-header">
                    <h3 className="tier-title">🎯 Tier 1: Perfect Matches</h3>
                    <p className="tier-subtitle">Highly relevant opportunities (80%+ match)</p>
                  </div>
                  {tier1.length > 0 ? (
                    <div className="results-grid">
                      {tier1.map((rec, index) => (
                        <RecommendationCard key={rec.internship_id} internship={rec} tier={1} />
                      ))}
                    </div>
                  ) : (
                    <div className="empty-state">No perfect matches found based on your exact profile.</div>
                  )}
                </div>

                {/* TIER 2 - Close Matches */}
                <div className="tier-section">
                  <div className="tier-header">
                    <h3 className="tier-title">✨ Tier 2: Close Matches</h3>
                    <p className="tier-subtitle">Good opportunities requiring some skill overlap (45% - 79% match)</p>
                  </div>
                  {tier2.length > 0 ? (
                    <div className="results-grid">
                      {tier2.map((rec, index) => (
                        <RecommendationCard key={rec.internship_id} internship={rec} tier={2} />
                      ))}
                    </div>
                  ) : (
                    <div className="empty-state">No close matches found in this tier.</div>
                  )}
                </div>

                {/* TIER 3 - Other Options */}
                <div className="tier-section">
                  <div className="tier-header">
                    <h3 className="tier-title">🔍 Tier 3: Other Options</h3>
                    <p className="tier-subtitle">Alternative roles in your sector/location (&lt;45% match)</p>
                  </div>
                  {tier3.length > 0 ? (
                    <div className="results-grid">
                      {tier3.map((rec, index) => (
                        <RecommendationCard key={rec.internship_id} internship={rec} tier={3} />
                      ))}
                    </div>
                  ) : (
                    <div className="empty-state">No other matching options available.</div>
                  )}
                </div>
              </>
            )}
          </section>
        )}

      </main>

      <footer className="footer">
        <p>Built for the <a href="https://pminternship.mca.gov.in/" target="_blank" rel="noopener noreferrer">PM Internship Scheme</a>.</p>
      </footer>
    </>
  );
}

export default App;
