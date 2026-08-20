import React, { useState } from 'react';

const CandidateForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    qualification: '',
    skills: '',
    sector_interested: '',
    location_interested: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="form-panel">
      <form onSubmit={handleSubmit} className="form-grid">
        
        <div className="form-group">
          <label className="form-label" htmlFor="qualification">Your Highest Education</label>
          <select 
            className="form-select" 
            id="qualification" 
            name="qualification"
            value={formData.qualification}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select Qualification</option>
            <option value="10th Pass">10th Pass</option>
            <option value="12th Pass">12th Pass</option>
            <option value="Diploma">Diploma</option>
            <option value="B.Tech">B.Tech</option>
            <option value="M.Tech">M.Tech</option>
            <option value="BBA">BBA</option>
            <option value="MBA">MBA</option>
            <option value="B.Pharma">B.Pharma</option>
            <option value="M.Pharma">M.Pharma</option>
            <option value="B.Design">B.Design</option>
            <option value="B.Sc">B.Sc</option>
            <option value="M.Sc">M.Sc</option>
            <option value="B.Com">B.Com</option>
            <option value="BA">BA</option>
            <option value="MA">MA</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="sector_interested">Interested Sectors</label>
          <select 
            className="form-select" 
            id="sector_interested" 
            name="sector_interested"
            value={formData.sector_interested}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select Sector</option>
            <option value="Information Technology">Information Technology</option>
            <option value="FinTech">FinTech</option>
            <option value="Marketing & Advertising">Marketing & Advertising</option>
            <option value="Data Science & Analytics">Data Science & Analytics</option>
            <option value="Human Resources">Human Resources</option>
            <option value="E-commerce">E-commerce</option>
            <option value="EdTech">EdTech</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Design">Design</option>
            <option value="Finance">Finance</option>
          </select>
        </div>

        <div className="form-group full-width">
          <label className="form-label" htmlFor="skills">Your Skills (e.g., Python, Marketing, AutoCAD)</label>
          <input 
            type="text" 
            className="form-input" 
            id="skills" 
            name="skills"
            placeholder="Enter skills separated by commas"
            value={formData.skills}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group full-width">
          <label className="form-label" htmlFor="location_interested">Preferred Location</label>
          <select 
            className="form-select" 
            id="location_interested" 
            name="location_interested"
            value={formData.location_interested}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select Location</option>
            <option value="Andhra Pradesh">Andhra Pradesh</option>
            <option value="Arunachal Pradesh">Arunachal Pradesh</option>
            <option value="Assam">Assam</option>
            <option value="Bihar">Bihar</option>
            <option value="Chhattisgarh">Chhattisgarh</option>
            <option value="Goa">Goa</option>
            <option value="Gujarat">Gujarat</option>
            <option value="Haryana">Haryana</option>
            <option value="Himachal Pradesh">Himachal Pradesh</option>
            <option value="Jharkhand">Jharkhand</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Kerala">Kerala</option>
            <option value="Madhya Pradesh">Madhya Pradesh</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Manipur">Manipur</option>
            <option value="Meghalaya">Meghalaya</option>
            <option value="Mizoram">Mizoram</option>
            <option value="Nagaland">Nagaland</option>
            <option value="Odisha">Odisha</option>
            <option value="Punjab">Punjab</option>
            <option value="Rajasthan">Rajasthan</option>
            <option value="Sikkim">Sikkim</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Telangana">Telangana</option>
            <option value="Tripura">Tripura</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
            <option value="Uttarakhand">Uttarakhand</option>
            <option value="West Bengal">West Bengal</option>
            <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
            <option value="Chandigarh">Chandigarh</option>
            <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
            <option value="Delhi">Delhi</option>
            <option value="Jammu and Kashmir">Jammu and Kashmir</option>
            <option value="Ladakh">Ladakh</option>
            <option value="Lakshadweep">Lakshadweep</option>
            <option value="Puducherry">Puducherry</option>
          </select>
        </div>
        
        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Find Matches ✨'}
        </button>
      </form>
    </div>
  );
};

export default CandidateForm;
