import React from 'react';

const RecommendationCard = ({ internship, tier }) => {
  const skills = internship.required_skills 
    ? internship.required_skills.split(',').map(s => s.trim()) 
    : [];

  return (
    <div className="rec-card">
      <div className="rec-card-header">
        <h3 className="rec-card-title">{internship.title}</h3>
        <span className={`match-badge tier-${tier}`}>
          {internship.match_percentage || 0}% Match
        </span>
      </div>
      
      <div className="rec-card-company">{internship.company_name}</div>
      
      <div className="rec-card-details">
        <div className="rec-card-detail">
          <strong>Sector:</strong> {internship.sector}
        </div>
        <div className="rec-card-detail">
          <strong>Location:</strong> {internship.location}
        </div>
      </div>
      
      <div className="rec-card-stipend">
        ₹ {internship.stipend?.toLocaleString('en-IN') || '0'} / month
      </div>
      
      <div className="rec-card-skills">
        {skills.slice(0, 4).map((skill, idx) => (
          <span key={idx} className="rec-card-skill-tag">{skill}</span>
        ))}
        {skills.length > 4 && (
          <span className="rec-card-skill-tag">+{skills.length - 4} more</span>
        )}
      </div>
      
      <a 
        href={internship.apply_link || '#'} 
        target="_blank" 
        rel="noopener noreferrer"
        className="apply-btn"
      >
        Apply on Portal
      </a>
    </div>
  );
};

export default RecommendationCard;
